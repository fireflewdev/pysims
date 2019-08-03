import pygame

def transparentify(image, alpha):
    copy = image.copy()
    copy.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
    return copy

#https://stackoverflow.com/questions/23056597/python-pygame-writing-text-in-sprite
#by KodyVanRy

class Text(pygame.sprite.Sprite):
    def __init__(self, text, size, color, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        self.font = pygame.font.SysFont("Arial", size)
        self.textSurf = self.font.render(text, 1, color)
        self.image = pygame.Surface((width, height))
        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        self.image.blit(self.textSurf, [width/2 - W/2, height/2 - H/2])

#https://stackoverflow.com/questions/12879225/pygame-applying-transparency-to-an-image-with-alpha
#by DR0ID
