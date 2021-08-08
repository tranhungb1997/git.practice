import datetime
from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views import View
from django.views.generic import ListView

from common.pagination import to_list_page
from main import settings_local
from shipment_app import models as shipment_model


def container_type_json(request):
    """
    Tạo chuỗi json container type sử dụng cho thẻ select containerType ở HTML
    :param request:
    :return: ContainerType Json
    """
    container_type_list = shipment_model.ContainerType.objects.all().values("slug", "size", "type_name")
    return JsonResponse(data=list(container_type_list), safe=False)


def city_json(request):
    """
    Tạo chuỗi json city sử dụng cho thẻ select orderPlace và destinationPlace ở HTML
    :param request:
    :return: City Json
    """
    city_list = shipment_model.City.objects.all().values("code", "country_name", "seaport_code")
    return JsonResponse(data=list(city_list), safe=False)


class SearchView(ListView):
    template_name = 'shipment/search.html' # render template
    model = shipment_model.ShipmentInfo # khai báo model
    context_object_name = 'shipment_info_list' # tên object trả về HTML
    paginate_by = 2 # giới hạn element trong 1 page

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Custom context (tạo thêm element trả về template)
        :param object_list:
        :param kwargs:
        :return: page_list, search_data
        """
        context = super(SearchView, self).get_context_data()
        page_range = context["page_obj"].paginator.page_range
        current_page = context["page_obj"].number
        context["page_list"] = to_list_page(page_range, current_page)
        context["search_data"] = dict(
            orgin_code=self.request.GET.get('orginPlace'),
            destination_code=self.request.GET.get('destinationPlace'),
            container_type=self.request.GET.get('containerType'))
        return context

    def get_queryset(self):
        """
        Custom câu query (đọc code để hiểu :D)
        :return: queryset
        """
        orgin_code = self.request.GET.get('orginPlace')
        destination_code = self.request.GET.get('destinationPlace')
        container_type = self.request.GET.get('containerType')
        orgin_data = shipment_model.City.objects.get(code=orgin_code)
        destination_data = shipment_model.City.objects.get(code=destination_code)
        try:
            routing_data = shipment_model.Routing.objects.get(orgin_place=orgin_data,
                                                              destination_place=destination_data)
        except Exception:
            raise Http404('Không tìm thấy kết quả tìm kiếm')
        if container_type is None or container_type == 'all':
            queryset = self.model.objects.filter(routing=routing_data, start_date__gte=date.today())
        else:
            container_type_data = shipment_model.ContainerType.objects.get(slug=container_type)
            queryset = self.model.objects.filter(routing=routing_data, type_container=container_type_data,
                                                 start_date__gte=date.today())
        for field in queryset:
            print(str(field.routing) + "|" + str(field.type_container) + "|" + str(field.start_date))
        return queryset

# class LoginRequiredMixin: tạo ràng buộc đăng nhập mới vào được class kế thừa
class Booking(LoginRequiredMixin, View):
    def get(self, request, id):
        """
        Khởi tạo trang booking
        :param request:
        :param id: sử dụng search thông tin shipment_info
        :return: template
        """
        try:
            shipment_info = shipment_model.ShipmentInfo.objects.get(id=id)
            return render(request, 'shipment/booking.html', {'shipment_info': shipment_info})
        except Exception:
            raise Http404('Thông tin booking không tồn tại')


class BookingConfirm(LoginRequiredMixin, View):
    def get(self, request):
        """
        Khởi tạo trang xác nhận thông tin booking và số lượng
        :param request:
        :return: template
        """
        booking_info = self.initial_booking_info(request)
        total = booking_info.amount * booking_info.shipment_info.price
        return render(request, 'shipment/booking-confirm.html', {'booking': booking_info, 'total': total})

    def post(self, request):
        """
        Lưu thông tin booking của khách hàng và gửi mail thông báo(khách hàng và admin)
        :param request:
        :return: template
        """
        booking_info = self.get_booking_info(request)
        user = request.user
        booking = shipment_model.Booking(shipment_info=booking_info.shipment_info, user=user,
                                         amount=booking_info.amount)
        booking.save()
        # Gửi mail admin
        subject = 'Thông báo có khách hàng booking'
        html_message = render_to_string('shipment/email_content/admin-email.html',
                                        {'booking': booking, 'today': datetime.now()})
        plain_message = strip_tags(html_message)
        from_email = settings_local.EMAIL_HOST_USER
        to = settings_local.ADMIN_EMAIL
        send_mail(subject=subject, message=plain_message, from_email=from_email, recipient_list=[to],
                  html_message=html_message)
        # Gửi mail khách hàng
        subject = 'Booking thành công (khách hàng)'
        html_message = render_to_string('shipment/email_content/customer-email.html',
                                        {'booking': booking, 'today': datetime.now()})
        plain_message = strip_tags(html_message)
        from_email = settings_local.EMAIL_HOST_USER
        to = booking.user.email
        send_mail(subject=subject, message=plain_message, from_email=from_email, recipient_list=[to],
                  html_message=html_message)
        return redirect('shipment_app:booking_success')

    def initial_booking_info(self, request):
        """
        Khởi tạo instance booking
        :param request:
        :return:
        """
        if request.method == 'GET':
            shipment_id = int(request.GET.get('shipmentId'))
            amount = int(request.GET.get('amount'))
            shipment_info = shipment_model.ShipmentInfo.objects.get(id=shipment_id)
            booking = shipment_model.Booking(shipment_info=shipment_info, amount=amount)
        else:
            shipment_id = int(request.POST.get('shipmentId'))
            amount = int(request.POST.get('amount'))
            shipment_info = shipment_model.ShipmentInfo.objects.get(id=shipment_id)
            booking = shipment_model.Booking(shipment_info=shipment_info, amount=amount)
        return booking


def error(request, exception):
    return render(request, 'error.html', {'errorMsg': exception})
