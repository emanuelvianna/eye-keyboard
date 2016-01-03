import pygame as pg

import settings as st


class EyeTracker(object):

    def __init__(self, camera_size):
        self.camera = self._get_camera(camera_size)
        self.camera.start()
        self.camera_size = self._get_camera_size(camera_size)
        self.threshold = st.DEFAULT_THRESHOLD
        self.pupil_pos = (-1, -1)
        self.pupil_rect = pg.Rect(
            self.camera_size[0] / 8 - 50,
            self.camera_size[1] / 8 - 25,
            st.DEFAULT_PUPIL_WIDTH,
            st.DEFAULT_PUPIL_HEIGHT
        )

    def _get_camera(self, camera_size):
        pg.camera.init()
        cameras = pg.camera.list_cameras()
        if not cameras:
            raise IOError("no available cameras")
        return pg.camera.Camera(cameras[0], camera_size, 'RGB')

    def _get_camera_size(self, camera_size):
        try:
            # `get_size` is not available in all systems
            return self.camera.get_size()
        except:
            return camera_size

    def give_me_all(self, use_prect=False):
        img = self.camera.get_image()
        thresholded = pg.surface.Surface(self.camera_size, 0, img)
        th = (self.threshold, self.threshold, self.threshold)
        pg.transform.threshold(
            thresholded, img, st.PUPIL_COLOUR, th, st.THRESHOLD_BACKGROUND_COLOUR, 1)

        self._find_pupil(thresholded, use_prect)
        return img, thresholded

    def _find_pupil(self, thresholded, use_prect=False):
        if use_prect:
            rectbounds = pg.Rect(self.pupil_rect)
            if self.pupil_rect.left < 0:
                rectbounds.left = 0
            if self.pupil_rect.right > self.camera_size[0]:
                rectbounds.right = self.camera_size[0]
            if self.pupil_rect.top < 0:
                rectbounds.top = 0
            if self.pupil_rect.bottom > self.camera_size[1]:
                rectbounds.bottom = self.camera_size[1]
            thresholded = thresholded.subsurface(rectbounds)
            ox, oy = thresholded.get_offset()
        th = (self.threshold, self.threshold, self.threshold)
        mask = pg.mask.from_threshold(thresholded, st.PUPIL_COLOUR, th)
        pupil = mask.connected_component()
        pupil_center = pupil.centroid()
        if use_prect:
            pupil_center = pupil_center[0] + ox, pupil_center[1] + oy
            if ((self.pupil_rect.left < pupil_center[0] < self.pupil_rect.right)
                    and (self.pupil_rect.top < pupil_center[1] < self.pupil_rect.bottom)):
                self.pupil_pos = pupil_center
                x = pupil_center[0] - self.pupil_rect[2] / 2
                y = pupil_center[1] - self.pupil_rect[3] / 2
                self.pupil_rect = pg.Rect(
                    x, y, self.pupil_rect[2], self.pupil_rect[3])
            else:
                self.pupil_pos = (-1, -1)
        else:
            self.pupil_pos = pupil_center
