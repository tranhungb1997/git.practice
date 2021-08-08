def to_list_page(page_range: range, current_page: int):
    """
    Tạo list page
    :param page_range:
    :param current_page:
    :return: page_list
    """
    # trang trước
    page_list = [dict(display="Trang trước", page=current_page - 1, enable=current_page > 1, active=False)]
    dot_flag = False
    # số trang
    for page in page_range:
        if page == min(page_range) or page == max(page_range) or (current_page - 2 < page < current_page + 2):
            dot_flag = False
            page_list.append(
                dict(display=str(page), page=page, enable=True, active=(page == current_page)))
        else:
            if not dot_flag:
                dot_flag = True
                page_list.append(
                    dict(display="...", page=None, enable=False, active=False))
            else:
                continue
    # trang sau
    page_list.append(dict(display="Trang sau", page=current_page + 1, enable=current_page < max(page_range), active=False))

    return page_list


