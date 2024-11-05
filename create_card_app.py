import marimo

__generated_with = "0.9.14"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    from PIL import Image, ImageDraw, ImageFont
    from io import BytesIO
    return BytesIO, Image, ImageDraw, ImageFont, mo


@app.cell
def __(
    birthday,
    card_id,
    fullname,
    img,
    mo,
    photo,
    photo_img,
    register_date,
    result_downloader,
    sex,
):
    mo.vstack(
        [
            mo.hstack(
                [
                    mo.vstack(
                        [
                            mo.hstack(["Имя Фамилия:", fullname]),
                            mo.hstack(["CARD NO.:", card_id]),
                            mo.hstack(["Дата рождения:", birthday]),
                            mo.hstack(["Дата регистрации карты:", register_date]),
                            mo.hstack(
                                ["Пол:", sex, ("Мужчина", "Женщина")[sex.value]],
                                justify="start",
                            ),
                            mo.hstack(["Upload photo", photo], justify="start"),
                            photo_img,
                        ]
                    ),
                    img,
                ],
                wrap=True,
            ),
            mo.right(result_downloader),
        ],
    )
    return


@app.cell
def __(ImageFont):
    def fnt(size, type_="Regular"):
        """
        Метод загрузки шрифта
        """
        f = ImageFont.truetype(f"./HarmonyOS_Sans_SC/HarmonyOS_Sans_SC_{type_}.ttf", size)
        return f
    return (fnt,)


@app.cell
def __(mo):
    # Создание полей ввода
    fullname = mo.ui.text(placeholder="Иван Иванов")
    card_id = mo.ui.text(placeholder="D123456789")
    birthday = mo.ui.date()
    register_date = mo.ui.date()
    sex = mo.ui.switch()
    photo = mo.ui.file(filetypes=[".jpg", ".jpeg", ".png"])
    return birthday, card_id, fullname, photo, register_date, sex


@app.cell
def __(BytesIO, img):
    def image_png_bytes():
        file = BytesIO()
        img.save(file, format='PNG')
        return file
    return (image_png_bytes,)


@app.cell
def __(fullname, image_png_bytes, mo):
    result_downloader = mo.download(
        data=image_png_bytes(),
        filename=f"{fullname.value.title().replace(' ', '_')}_id_card.png",
        mimetype="image/png",
        label="Скачать",
    )
    return (result_downloader,)


@app.cell
def __(BytesIO, Image, photo):
    # Настройки загрузки фотографии
    photosize = (169, 198)
    photo_img = Image.new("RGBA", photosize, (255, 255, 255, 255))
    if photo.value:
        photo_img_n = Image.open(BytesIO(photo.value[0].contents))
        # Если ширина больше чем надо
        if photo_img_n.size[0] / photo_img_n.size[1] > photosize[0] / photosize[1]:
            _width = photosize[0]
            _height = photo_img_n.size[1] / photo_img_n.size[0] * photosize[0]
        else:
            _height = photosize[1]
            _width = photo_img_n.size[0] / photo_img_n.size[1] * photosize[1]
        photo_img_n = photo_img_n.resize((int(_width), int(_height)))
        photo_img.paste(photo_img_n, ((photosize[0] - photo_img_n.size[0])//2, (photosize[1] - photo_img_n.size[1])//2))
    return photo_img, photo_img_n, photosize


@app.cell
def __(
    Image,
    ImageDraw,
    birthday,
    card_id,
    fnt,
    fullname,
    photo_img,
    photosize,
    register_date,
    sex,
):
    # Заполнение карточки
    img = Image.open("./Шаблон-ID-Card-Доминики-пустой.png").convert("RGBA")
    draw = ImageDraw.Draw(img)

    # fullname
    draw.text(
        (254, 153),
        fullname.value.upper().replace(" ", "  "),
        font=fnt(25),
        fill=(0, 0, 0, 255),
    )
    # birthday
    draw.text(
        (314, 200),
        birthday.value.strftime("%b %d %Y").replace(" 0", " "),
        font=fnt(19),
        fill=(0, 0, 0, 255),
    )
    # sex
    draw.text((316, 231), ("M", "W")[sex.value], font=fnt(20), fill=(0, 0, 0, 255))
    # dominic id
    # register
    draw.text(
        (319, 264),
        register_date.value.strftime("%b %d %Y").replace(" 0", " "),
        font=fnt(19),
        fill=(0, 0, 0, 255),
    )
    # register end
    draw.text(
        (319, 296),
        f'{register_date.value.strftime("%b %d").replace(" 0", " ")} {register_date.value.year+3}',
        font=fnt(19),
        fill=(0, 0, 0, 255),
    )

    # card no
    # UP
    for n, sym in enumerate(card_id.value):
        draw.text(
            (449 + n * 12 - n // 4, 61),
            sym,
            font=fnt(15, "Bold"),
            fill=(0, 0, 0, 255),
        )
    # DOWN
    for n, sym in enumerate(card_id.value):
        draw.text(
            (503 + n * 12 - n // 4, 331),
            sym,
            font=fnt(15, "Medium"),
            fill=(134, 152, 138, 255),
        )
    _left_corner = 58, 126
    img.paste(photo_img, (*_left_corner, _left_corner[0]+photosize[0], _left_corner[1]+photosize[1]))
    return draw, img, n, sym


if __name__ == "__main__":
    app.run()
