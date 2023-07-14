import streamlit as st
import requests
import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import time
from streamlit_lottie import st_lottie

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

st.set_page_config(
    page_title="A.Iris",
    page_icon="A.I",
    layout="wide",
    initial_sidebar_state="expanded",
)



lottie_welcome = load_lottieurl(
    "https://assets9.lottiefiles.com/packages/lf20_ufkjsujv.json"
)


st.title("A.Iris: Detecting eye diseases")
st_lottie(lottie_welcome, height=300, key="welcome")

def main():
    # st.title("A.Iris")
    # st.write("------------------------------------------")
    # st.sidebar.title("")
    choices = ["Home","DR", "Cataract", "Redness"]
    menu = st.sidebar.selectbox("Menu: ", choices)
    st.set_option('deprecation.showfileUploaderEncoding', False)
    if menu =="Home":
        st.write("A.Iris helps you detect three major types of eye diseases, namely cataract, diabetic retinopathy and redness levels. ")
        
        def search_op(location, radius=10):
            url = f"https://nominatim.openstreetmap.org/search?q={location}&format=json&limit=1"
            response = requests.get(url)
            result = response.json()
            if not result:
                return []
            name = ""
            place = result[0]
            latitude, longitude = float(place["lat"]), float(place["lon"])

            url = f"https://nominatim.openstreetmap.org/search?q=opthalmologist&format=json&limit=10&viewbox={longitude - radius},{latitude - radius},{longitude + radius},{latitude + radius}"
            response = requests.get(url)
            result = response.json()
            if not result:
                return []
            
            op = []
            for place in result:
                if location.lower() in place["display_name"].lower():
                    op.append({
                        "name": place["display_name"],
                        "latitude": float(place["lat"]),
                        "longitude": float(place["lon"]),
                        "address": place.get("address", {}).get("road", ""),
                    })
            return op

        def main():
            
            st.write("------------------------------------------")
            st.title("Find Ophthalmologist Near You")

            location = st.text_input("Enter a location:")
            # radius = st.slider("Radius (km):", 0, 50, 10)

            if location:
                op = search_op(location)
                if op:
                    st.write("Opthalmologists in your area:")
                    for op in op:
                        st.write("-", op["name"])
                else:
                    st.write("No ophthalmologist found in your area.")

        if __name__ == '__main__':
            main()
    

    
    elif menu == "Cataract":
        st.title("Detect Cataract")
        st.sidebar.write("A cataract is a cloudy area in the lens of a person's eye")
        st.write("---------------------------")
        image_input = st.file_uploader("Choose an eye image: ", type="jpg")
        if image_input:
            img = image_input.getvalue()
            st.sidebar.image(img, width=300)
            np.set_printoptions(suppress=True)
            model = tensorflow.keras.models.load_model('eye_models/cataract/model.h5')
            data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
            image = Image.open(image_input)
            size = (224, 224)
            image = ImageOps.fit(image, size, Image.ANTIALIAS)
            image_array = np.asarray(image)
            normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
            data[0] = normalized_image_array
            size = st.slider("Adjust Image Size: ", 300, 1000)
            st.image(img, width=size)
            st.write("------------------------------------------------------")
            detect = st.button("Detect Cataract")
            if detect:
                prediction = model.predict(data)
                class1 = prediction[0,0]
                class2 = prediction[0,1]
                if class1 > class2:
                    st.markdown("A.Iris thinks this is a **Cataract** by {:.2f}%".format(class1 * 100) )
                elif class2 > class1:
                    st.markdown("A.Iris thinks this is not **Cataract** by {:.2f}%".format(class2 * 100))
                else:
                    st.write("We encountered an ERROR. This should be temporary, please try again with a better quality image. Cheers!")
                    
                
    elif menu == "DR":
        st.title("Detect Diabetic Retinopathy")
        st.sidebar.write("Diabetic retinopathy is caused by damage to the blood vessels in the tissue at the back of the eye (retina). ")
        st.write("---------------------------")
        image_input = st.file_uploader("Choose an eye image: ", type=["jpg","png","jpeg"])
        if image_input:
            img = image_input.getvalue()
            st.sidebar.image(img, width=300)
            np.set_printoptions(suppress=True)
            model = tensorflow.keras.models.load_model('eye_models/cataract/model.h5')
            data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
            image = Image.open(image_input)
            size = (224, 224)
            image = ImageOps.fit(image, size, Image.ANTIALIAS)
            image_array = np.asarray(image)
            normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
            data[0] = normalized_image_array
            size = st.slider("Adjust Image Size: ", 300, 1000)
            st.image(img, width=size)
            st.write("------------------------------------------------------")
            dr = st.button("Analyze Diabetic Retinopathy")

            if dr:
                model_d = tensorflow.keras.models.load_model('eye_models/dr/model.h5')
                data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
                image = Image.open(image_input)
                size = (224, 224)
                image = ImageOps.fit(image, size, Image.ANTIALIAS)
                image_array = np.asarray(image)
                normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
                data[0] = normalized_image_array
                answer = model_d.predict(data)
                class1 = answer[0,0]
                class2 = answer[0,1]
                if class1 > class2:
                    st.write("Diabetic Retinopathy Detected. Confidence: {:.2f}".format(class1 * 100))
                    if (class1 * 100) > 50 and (class1 * 100) < 60 :
                        st.write("Severity level: 1")
                    
                    if (class1 * 100) > 60 and (class1 * 100) < 75 :
                        st.write("Severity level: 2")
                        
                    if (class1 * 100) > 75 and (class1 * 100) < 90 :
                        st.write("Severity level: 3")
                        
                    if (class1 * 100) > 90 and (class1 * 100) < 100 :
                        st.write("Severity level: 4")
                    
                    st.write("-------------------------------")
                elif class2 > class1:
                    st.write("Diabetic Retinopathy Not Detected.")
                    st.write("-------------------------------")
            
                
    elif menu == "Redness":
        st.title("Detect Redness")
        st.sidebar.write("The redness happens when tiny blood vessels under the eye's surface get larger or become inflamed.")
        st.write("---------------------------")
        image_input = st.file_uploader("Choose an eye image: ", type="jpg")
        if image_input:
            img = image_input.getvalue()
            st.sidebar.image(img, width=300)
            np.set_printoptions(suppress=True)
            model = tensorflow.keras.models.load_model('eye_models/cataract/model.h5')
            data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
            image = Image.open(image_input)
            size = (224, 224)
            image = ImageOps.fit(image, size, Image.ANTIALIAS)
            image_array = np.asarray(image)
            normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
            data[0] = normalized_image_array
            size = st.slider("Adjust Image Size: ", 300, 1000)
            st.image(img, width=size)
            st.write("------------------------------------------------------")
            r = st.button("Analyze Redness Levels")            
                
            if r:
                model_r = tensorflow.keras.models.load_model('eye_models/redness/model.h5')
                data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
                image = Image.open(image_input)
                size = (224, 224)
                image = ImageOps.fit(image, size, Image.ANTIALIAS)
                image_array = np.asarray(image)
                image.show()
                normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
                data[0] = normalized_image_array
                answer = model_r.predict(data)
                class1 = answer[0,0]
                class2 = answer[0,1]
                if class1 > class2:
                    st.write("Redness Levels: {:.2f}%".format(class1 * 100))
                    st.write("-------------------------------")
                elif class2 > class1:
                    st.write("No Redness Detected. Confidence: {:.2f}%".format(class2 * 100))
                    st.write("-------------------------------")


if __name__ == '__main__':
    main()
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
            
            
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
