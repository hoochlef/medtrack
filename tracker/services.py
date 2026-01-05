from ollama import ChatResponse, chat
from paddleocr import PaddleOCR

_ocr_engine = PaddleOCR(
    text_detection_model_name="PP-OCRv5_mobile_det",
    text_recognition_model_name="PP-OCRv5_mobile_rec",
    # images may be uploaded sideways or even upside down
    # from users
    use_doc_orientation_classify=True,
    # some medication comes in conic shapes and it needs
    # to be flattened in order for the model to extract text
    use_doc_unwarping=True,
    use_textline_orientation=False,
    text_det_limit_side_len=960,
    text_det_limit_type="max",
)


def run_ocr(image_array):
    """run ocr on uploaded image"""
    try:
        result = _ocr_engine.predict(image_array)
    except RuntimeError:
        print("Runtime Error")
    if result and len(result) > 0:
        first_page = result[0]

        # pull the list of recognized strings directly
        if "rec_texts" in first_page:
            return (
                ", ".join(first_page["rec_texts"])
                if first_page["rec_texts"]
                else "No text found."
            )

    return []


def run_custom_slm(ocr_output):
    """A function to run the small language model on the ocr output and return a
    result"""
    response: ChatResponse = chat(
        model="llama3.2:3b-med-v0",
        messages=[
            {
                "role": "user",
                "content": f"{ocr_output}",
            },
        ],
    )
    return response.message.content
