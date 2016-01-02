import pygame
import pygame.camera

import settings as st


class EyeTracker(object):  # PUPIL TRACKER

    def __init__(self, camera_size):
        self.camera = None
        self.threshold = st.DEFAULT_THRESHOLD
        self.pupil_pos = (-1, -1)

        self._init_camera(camera_size)
        self._init_camera_size_treating_os_compatibilities(camera_size)

        self.settings = {
            'nonthresholdcol': (100, 100, 255, 255),
            'pupilrect': pygame.Rect(
                self.camera_size[0] / 8 - 50, self.camera_size[1] / 8 - 25, 25, 12),
            'pupilbounds': [0, 0, 0, 0],
            '': None
        }

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

    def give_me_all(self, pupilrect=False):
        snapshot = self.camera.get_image()
        thresholded = pygame.surface.Surface(self.camera_size, 0, snapshot)
        th = (self.threshold, self.threshold, self.threshold)
        pygame.transform.threshold(
            thresholded, snapshot, st.PUPIL_COLOUR, th, self.settings['nonthresholdcol'], 1)
        pupilsize, pupilbounds = self._find_pupil(thresholded, pupilrect)
        return snapshot, thresholded, pupilsize, pupilbounds

    def _find_pupil(self, thresholded, pupilrect=False):
        if pupilrect:
            rectbounds = pygame.Rect(self.settings['pupilrect'])
            if self.settings['pupilrect'].left < 0:
                rectbounds.left = 0
            if self.settings['pupilrect'].right > self.camera_size[0]:
                rectbounds.right = self.camera_size[0]
            if self.settings['pupilrect'].top < 0:
                rectbounds.top = 0
            if self.settings['pupilrect'].bottom > self.camera_size[1]:
                rectbounds.bottom = self.camera_size[1]
            thresholded = thresholded.subsurface(rectbounds)
            ox, oy = thresholded.get_offset()
        th = (self.threshold, self.threshold, self.threshold)
        mask = pygame.mask.from_threshold(thresholded, st.PUPIL_COLOUR, th)
        pupil = mask.connected_component()
        pupilcenter = pupil.centroid()
        if pupilrect:
            pupilcenter = pupilcenter[0] + ox, pupilcenter[1] + oy
            if (self.settings['pupilrect'].left < pupilcenter[0] < self.settings['pupilrect'].right) and (self.settings['pupilrect'].top < pupilcenter[1] < self.settings['pupilrect'].bottom):
                self.pupil_pos = pupilcenter
                x = pupilcenter[0] - self.settings['pupilrect'][2] / 2
                y = pupilcenter[1] - self.settings['pupilrect'][3] / 2
                self.settings['pupilrect'] = pygame.Rect(
                    x, y, self.settings['pupilrect'][2], self.settings['pupilrect'][3])
            else:
                self.pupil_pos = (-1, -1)
        else:
            self.pupil_pos = pupilcenter
        try:
            self.settings['pupilbounds'] = pupil.get_bounding_rects()[0]
            if pupilrect:
                self.settings['pupilbounds'].left += ox
                self.settings['pupilbounds'].top += oy
        except:
            pass
        return pupil.count(), self.settings['pupilbounds']
