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
    result = _ocr_engine.predict(image_array)

    if result and len(result) > 0:
        first_page = result[0]

        # pull the list of recognized strings directly
        if "rec_texts" in first_page:
            return first_page["rec_texts"]

    return []
