# Импорт библиотек
import streamlit as st 
from PIL import Image
from io import BytesIO
import numpy as np
import cv2

# Функция для создания эффекта акварели
def convert_to_watercolor_sketch(inp_img, sigma_s, sigma_r):
    img_1 = cv2.edgePreservingFilter(inp_img, flags=2, sigma_s=sigma_s, sigma_r=0.8)
    img_water_color = cv2.stylization(img_1, sigma_s=sigma_s, sigma_r=sigma_r) # функция для стилизации изображения, создающая эффект акварели
    return img_water_color

# Функция для конвертации изображения в карандашный эскиз
def pencil_sketch(inp_img, sigma_s, sigma_r, shade_factor):
    img_pencil_sketch, _ = cv2.pencilSketch(inp_img, sigma_s=sigma_s, sigma_r=sigma_r, shade_factor=shade_factor) # функция, создающая эффект карандашного рисунка
    return img_pencil_sketch

# Функция для применения эффекта сепии
def sepia_effect(inp_img):
    kernel = np.array([[0.272, 0.534, 0.131],
                       [0.349, 0.686, 0.168],
                       [0.393, 0.769, 0.189]])
    sepia_img = cv2.transform(inp_img, kernel)
    sepia_img = np.clip(sepia_img, 0, 255)
    return sepia_img

# Функция для загрузки изображения
def load_an_image(image):
    img = Image.open(image)
    return img

# Основная функция, реализующая веб-приложение
def main():
    # Заголовки и описание приложения
    st.title('Веб-приложение для конвертации изображений')
    st.write("Это приложение для преобразования вашего ***изображения*** в ***Акварельный эскиз***, ***Карандашный эскиз*** или ***Эффект Сепии***.")
    st.subheader("Пожалуйста, загрузите ваше изображение")

    # Загрузка изображения
    image_file = st.file_uploader("Загрузите изображение", type=["png", "jpg", "jpeg"])

    # Если изображение загружено
    if image_file is not None:
        image = Image.open(image_file)
        img_array = np.array(image)

        # Выбор эффекта
        option = st.selectbox('Выберите тип конвертации изображения',
                              ('Акварельный эскиз', 'Карандашный эскиз', 'Эффект Сепии'))

        # Параметры для акварельного эскиза
        if option == 'Акварельный эскиз':
            sigma_s = st.slider('Интенсивность сглаживания', 0, 200, 100)
            sigma_r = st.slider('Интенсивность детализации', 0.0, 1.0, 0.5)
            final_sketch = convert_to_watercolor_sketch(img_array, sigma_s, sigma_r)

        # Параметры для карандашного эскиза
        elif option == 'Карандашный эскиз':
            sigma_s = st.slider('Интенсивность сглаживания', 0, 200, 50)
            sigma_r = st.slider('Интенсивность детализации', 0.0, 1.0, 0.07)
            shade_factor = st.slider('Интенсивность затемнения', 0.0, 0.1, 0.05)
            final_sketch = pencil_sketch(img_array, sigma_s, sigma_r, shade_factor)

        # Эффект сепии
        elif option == 'Эффект Сепии':
            final_sketch = sepia_effect(img_array)

        # Показ оригинального и обработанного изображений
        col1, col2 = st.columns(2)
        with col1:
            st.header("Оригинальное изображение")
            st.image(image, width=350)

        with col2:
            st.header(option)
            st.image(final_sketch, width=350)

        # Сохранение обработанного изображения
        buf = BytesIO()
        img_pil = Image.fromarray(final_sketch)
        img_pil.save(buf, format="JPEG")
        byte_im = buf.getvalue()
        st.download_button(label="Скачать изображение",
                           data=byte_im,
                           file_name=f"{option.lower().replace(' ', '_')}.png",
                           mime="image/pnыg")

if __name__ == '__main__':
    main()
