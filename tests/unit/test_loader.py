from app.services.pipeline_loader import get_pipeline, get_feature_names

def test_loader():
    pipe = get_pipeline()
    cols = get_feature_names()
    assert hasattr(pipe, "predict")
    assert isinstance(cols, list) and len(cols) > 0
