import pygame
import pygame.camera

import settings as st


class EyeTracker(object):  # PUPIL TRACKER

    def __init__(self, camera_size):
        # self.camera = None
        # self.camera_size = None

        self._init_camera(camera_size)
        self._init_camera_size_treating_os_compatibilities(camera_size)

        self.threshold = st.DEFAULT_THRESHOLD
        self.pupil_pos = (-1, -1)
        self.pupil_rect = pygame.Rect(
            self.camera_size[0] / 8 - 50,
            self.camera_size[1] / 8 - 25,
            st.DEFAULT_PUPIL_WIDTH,
            st.DEFAULT_PUPIL_HEIGHT
        )

    def _init_camera(self, camera_size):
        pygame.camera.init()
        cameras = pygame.camera.list_cameras()
        if not cameras:
            raise IOError("no available cameras")
        self.camera = pygame.camera.Camera(cameras[0], camera_size, 'RGB')
        self.camera.start()

    def _init_camera_size_treating_os_compatibilities(self, camera_size):
        try:
            # get size is not available in all systems
            self.camera_size = self.camera.get_size()
        except:
            self.camera_size = camera_size

    def give_me_all(self, use_prect=False):
        snapshot = self.camera.get_image()
        thresholded = pygame.surface.Surface(self.camera_size, 0, snapshot)
        th = (self.threshold, self.threshold, self.threshold)
        pygame.transform.threshold(
            thresholded, snapshot, st.PUPIL_COLOUR, th, st.THRESHOLD_BACKGROUND_COLOUR, 1)
        pupilsize = self._find_pupil(thresholded, use_prect)
        return snapshot, thresholded, pupilsize

    def _find_pupil(self, thresholded, use_prect=False):
        if use_prect:
            rectbounds = pygame.Rect(self.pupil_rect)
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
        mask = pygame.mask.from_threshold(thresholded, st.PUPIL_COLOUR, th)
        pupil = mask.connected_component()
        pupil_center = pupil.centroid()
        if use_prect:
            pupil_center = pupil_center[0] + ox, pupil_center[1] + oy
            if ((self.pupil_rect.left < pupil_center[0] < self.pupil_rect.right)
                    and (self.pupil_rect.top < pupil_center[1] < self.pupil_rect.bottom)):
                self.pupil_pos = pupil_center
                x = pupil_center[0] - self.pupil_rect[2] / 2
                y = pupil_center[1] - self.pupil_rect[3] / 2
                self.pupil_rect = pygame.Rect(
                    x, y, self.pupil_rect[2], self.pupil_rect[3])
            else:
                self.pupil_pos = (-1, -1)
        else:
            self.pupil_pos = pupil_center
        return pupil.count()
