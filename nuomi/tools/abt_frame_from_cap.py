import os
import os.path as osp
import cv2 as cv
import time


def abt_frame_cap(save_dir, step=30):
    if not osp.exists(save_dir):
        os.makedirs(save_dir)

    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Can't Open Camera!!!")
        return 
    cnt = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Camera Can't Read!!!")
            break
        
        cv.imshow("frame", frame)
        if cv.waitKey(1) == 27:
            cv.destroyAllWindows()
            break
        
        if cnt % step == 0:
            datetime = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
            save_path = osp.join(save_dir, f"{datetime}_{str(cnt//step).zfill(8)}.jpg")
            print(f"===> save frame {cnt} in: {save_path}")
            cv.imwrite(save_path, frame)
        cnt += 1
    cap.release()
    


if __name__ == "__main__":
    save_dir = ""
    step = 20
    abt_frame_cap(save_dir, step)
