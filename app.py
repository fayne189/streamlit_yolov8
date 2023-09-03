import cv2
import torch
import streamlit as st
from ultralytics import YOLO
from ui import MainUi
import utils

# init global variables and store in session state
device = st.session_state.get('device')
if device is None:
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    st.session_state['device'] = device

cfg = st.session_state.get('cfg')
if cfg is None:
    cfg = utils.load_config()  # yaml
    st.session_state['cfg'] = cfg


class MyModel(object):
    '''
    负责画面呈现, 条件判断及行为执行 
    '''
    def __init__(self, model):
        self.model = model

    def inference(self, frame, conf=0.5, tracker=''):
        # 得到模型输出的boxes及tracker_id
        if tracker:
            res = self.model.track(frame, persist=True, conf=conf, tracker=tracker)
        else:
            res = self.model.predict(frame, conf=conf, show_conf=True)
        res_frame = res[0].plot()
        return res_frame
        

@st.cache_resource
def init_model(model_path, device):
    if model_path:
        model = YOLO(model_path)
        model.to(device)
        return MyModel(model)

@st.cache_resource
def get_video_frames(file_name):
    frames = []
    vid_cap = cv2.VideoCapture(file_name)
    while (vid_cap.isOpened()):
        success, image = vid_cap.read()
        if success:
            frames.append(image)
        else:
            vid_cap.release()
            break
    return frames

def main():
    # get global variables
    cfg = st.session_state.cfg
    device = st.session_state.device


    # init UI
    main_ui = MainUi(cfg)

    # init monitor and model
    model_path = main_ui.model_path
    model = init_model(model_path, device)


    # init frames from video_path
    video_path = main_ui.video_path
    if video_path:
        frames = get_video_frames(video_path)
        selected_frames, selected_frame_index = main_ui.frame_selector_sidebar(frames)        
        selected_frame = frames[selected_frame_index]
        main_ui.show(selected_frame.copy())

        # inference on click button
        if main_ui.button_predict_one:
            result = model.inference(selected_frame.copy(),conf=main_ui.confidence_threshold, tracker=main_ui.use_tracker)
            main_ui.show(result)

        if main_ui.button_predict_all:
            for frame in selected_frames:
                if main_ui.button_stop:
                    break
                result = model.inference(frame.copy(),conf=main_ui.confidence_threshold, tracker=main_ui.use_tracker)
                main_ui.show(result)







if __name__ == '__main__':
    main()