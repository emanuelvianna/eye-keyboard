import pygame
import pygame.camera


class EyeTracker(object):

    def __init__(self, camera_size):
        """
        Creates a eye tracker controller.

        Parameters
        ----------
        camera_size: (int, int)
            Camera camera_size height and width

        Raises
        ------
        IOError
            if not found an available camera
        """
        self._init_camera(camera_size)
        self._init_camera_size_treating_os_compatibilities(camera_size)

        self.settings = {
            'pupilcol': (0, 0, 0),
            'threshold': 100,
            'nonthresholdcol': (100, 100, 255, 255),
            'pupilpos': (-1, -1),
            'pupilrect': pygame.Rect(
                self.camera_size[0] / 2 - 50, self.camera_size[1] / 2 - 25, 100, 50),
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
        th = (self.settings['threshold'], self.settings['threshold'], self.settings['threshold'])
        pygame.transform.threshold(
            thresholded, snapshot, self.settings['pupilcol'], th, self.settings['nonthresholdcol'], 1)
        pupilpos, pupilsize, pupilbounds = self._find_pupil(thresholded, pupilrect)
        return snapshot, thresholded, pupilpos, pupilsize, pupilbounds

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
        th = (self.settings['threshold'], self.settings['threshold'], self.settings['threshold'])
        mask = pygame.mask.from_threshold(thresholded, self.settings['pupilcol'], th)
        pupil = mask.connected_component()
        pupilcenter = pupil.centroid()
        if pupilrect:
            pupilcenter = pupilcenter[0] + ox, pupilcenter[1] + oy
            if (self.settings['pupilrect'].left < pupilcenter[0] < self.settings['pupilrect'].right) and (self.settings['pupilrect'].top < pupilcenter[1] < self.settings['pupilrect'].bottom):
                self.settings['pupilpos'] = pupilcenter
                x = pupilcenter[0] - self.settings['pupilrect'][2] / 2
                y = pupilcenter[1] - self.settings['pupilrect'][3] / 2
                self.settings['pupilrect'] = pygame.Rect(
                    x, y, self.settings['pupilrect'][2], self.settings['pupilrect'][3])
            else:
                self.settings['pupilpos'] = (-1, -1)
        else:
            self.settings['pupilpos'] = pupilcenter
        try:
            self.settings['pupilbounds'] = pupil.get_bounding_rects()[0]
            if pupilrect:
                self.settings['pupilbounds'].left += ox
                self.settings['pupilbounds'].top += oy
        except:
            pass
        return self.settings['pupilpos'], pupil.count(), self.settings['pupilbounds']
