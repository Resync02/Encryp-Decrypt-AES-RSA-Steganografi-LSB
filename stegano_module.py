from stegano import lsb

def hide_data(
        image_path,
        secret_data,
        output_image
):

    secret = lsb.hide(
        image_path,
        secret_data
    )

    secret.save(output_image)

def reveal_data(image_path):

    return lsb.reveal(image_path)