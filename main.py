import pygame
from pygame import Rect, Surface, Vector2, Color
from math import radians, sin, cos, pi
from numpy import arange


class Circle:
    def __init__(self, pos: Vector2, radius: int, mod: int) -> None:
        self.radius = radius
        self.rect = Rect(pos, Vector2(radius * 2, radius * 2))
        self.mod = mod
        self.frame: int = 0
        self.points: list[Vector2] = [
            Vector2(
                radius * cos(i) + self.rect.centerx,
                radius * sin(i) + self.rect.centery,
            )
            for i in arange(0, 2 * pi, 2 * pi / 360)
        ]
        self.time_delay_from_drawn = 90

    def animate(self, screen: Surface):
        if self.frame < 90:
            pygame.draw.arc(
                screen, Color("white"), self.rect, 0, radians(self.frame * 4)
            )
        else:
            pygame.draw.circle(screen, Color("white"), self.rect.center, self.radius, 1)
            for nth_point in range(
                min((self.frame - self.time_delay_from_drawn), len(self.points))
            ):
                pygame.draw.aaline(
                    screen,
                    Color("white"),
                    self.points[nth_point],
                    self.points[(nth_point * self.mod) % len(self.points)],
                )
        self.frame += 1


def main():

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Circle Pattern")
    running = True
    clock = pygame.time.Clock()

    width = 10
    height = 5
    top_border = 5
    side_border = 5
    radius = min(
        screen.get_height() / (height * 2) - (2 * top_border),
        screen.get_width() / (width * 2) - (2 * side_border),
    )
    diameter = radius * 2
    spacing = max(
        (screen.get_height() - (height * diameter)) / height,
        (screen.get_width() - (width * diameter)) / width,
    )
    center = Vector2(screen.get_width() / 2, screen.get_height() / 2)
    circles: list[Circle] = []
    start = Vector2(center.x - (width * radius) - (2 * spacing), top_border)
    for i in range(height):
        for j in range(width):
            circles.append(
                Circle(
                    start
                    + Vector2(
                        diameter * j + (j * spacing), diameter * i + (i * spacing)
                    ),
                    radius,
                    (i * width) + j + 2,
                )
            )

    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LCTRL]:
            running = False

        screen.fill((0, 0, 0))

        for circle in circles:
            circle.animate(screen)

        pygame.display.flip()
    pygame.quit()


main()
