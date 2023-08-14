def show_button(url):
    return f'<a type="button" class="btn mb-2 btn-outline-link" href="javascript:void(0);" onclick="complete(\'{url}\')"><i class="bx bx-check"></i></a>'


def edit_button(url):
    return f'<a type="button" class="btn mb-2 btn-outline-link" href="javascript:void(0);" onclick="commonEdit(\'{url}\')"><i class="bx bx-edit-alt"></i></a>'


def delete_button(url):
    return f'<a type="button" class="btn mb-2 btn-outline-link" href="javascript:void(0);" onclick="commonDelete(\'{url}\')"><i class="bx bx-trash-alt"></i></a>'