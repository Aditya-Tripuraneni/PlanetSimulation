import pygame
import math
import requests

WIDTH, HEIGHT = 2000, 1000

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet simulator")

request = requests.get("http://api.open-notify.org/astros.json")
data = request.json()

background = pygame.image.load("backgroundSpace.jpg")

RED = (255, 0, 0)
VIOLET = (148, 0, 211)
INDIGO = (75, 0, 130)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 127, 0)
WHITE = (255, 255, 255)
GREY = (192, 192, 192)

FPS = 60
run = True

pygame.init()
clock = pygame.time.Clock()

default = 24

G = 6.67428e-11
AU = 149.6e6 * 1000
SCALE = 120 / AU
TIMESTEP = 3600 * 24  # seconds in day

FONT = pygame.font.SysFont("comicsansms", 13)


class Planet:
    def __init__(self, x, y, mass, colour, radius):
        self.x = x
        self.y = y
        self.mass = mass
        self.colour = colour
        self.radius = radius
        self.x_vel = 0
        self.y_vel = 0
        self.distance_to_sun = 0
        self.is_sun = False
        self.forces = []

    def draw_planet(self, window):
        x = self.x * SCALE + WIDTH / 2
        y = self.y * SCALE + HEIGHT / 2
        pygame.draw.circle(window, self.colour, (x, y), self.radius)

        new_points = []

        if len(self.forces) > 2:
            for coordinate in self.forces:
                x, y = coordinate
                x = x * SCALE + WIDTH // 2
                y = y * SCALE + HEIGHT // 2
                new_points.append((x, y))
            pygame.draw.lines(window, WHITE, False, new_points, 3)

        if not self.is_sun:
            text = FONT.render(f"{round(self.distance_to_sun / 1000)}km", True, ORANGE)
            window.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2 * SCALE))

    def calculate_force_attraction(self, other_planet):
        other_planet_X, other_planet_Y = other_planet.x, other_planet.y
        distance_X = other_planet_X - self.x
        distance_Y = other_planet_Y - self.y
        distance = math.sqrt(distance_X ** 2 + distance_Y ** 2)

        if other_planet.is_sun:
            self.distance_to_sun = distance


        force = G * self.mass * other_planet.mass / distance ** 2
        angle = math.atan2(distance_Y, distance_X)
        fx = force * (math.cos(angle))
        fy = force * (math.sin(angle))

        return fx, fy

    def update_position(self, planets):
        fxtotal = fytotal = 0

        for planet in planets:
            if self is planet:
                continue
            fx, fy = self.calculate_force_attraction(planet)
            fxtotal += fx
            fytotal += fy
        # f = ma
        self.x_vel += fxtotal / self.mass * TIMESTEP
        self.y_vel += fytotal / self.mass * TIMESTEP

        self.x += self.x_vel * TIMESTEP
        self.y += self.y_vel * TIMESTEP
        self.forces.append((self.x, self.y))


def display_data(window):
    num_people_in_space = data['number']
    list_of_data = data['people']
    peoples_name = """"""
    for info in list_of_data:
        peoples_name += info['name'] + " "

    num_people = FONT.render(f"Current people in space: {num_people_in_space}", True, GREEN)
    names = FONT.render(f"Astronauts: {peoples_name}", True, GREEN)
    screen.blit(num_people, (0, 0))
    screen.blit(names, (0, 20))


sun = Planet(0, 0, 1.98892e30, YELLOW, 30)
sun.is_sun = True

earth = Planet(-1 * AU, 0, 5.9742e24, BLUE, 16)
earth.y_vel = 29.783e3

mercury = Planet(.387 * AU, 0, 3.30e23, GREY, 9)
mercury.y_vel = 47.4e3

venus = Planet(0.723 * AU, 0, 4.8685e24, ORANGE, 12)
venus.y_vel = -35.02e3

mars = Planet(-1.524 * AU, 0, 6.39e23, RED, 14)
mars.y_vel = 24.077e3

jupiter = Planet(4.2 * AU, 0, 1.89e24, GREEN, 20)
jupiter.y_vel = -13.6e3



planets = [sun, earth, mercury, venus, mars, jupiter]

while run:
    clock.tick(FPS)
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_h]:
        TIMESTEP = 3600
    if keys[pygame.K_d]:
        TIMESTEP = 3600 * 24
    for planet in planets:
        planet.update_position(planets)
        planet.draw_planet(screen)

    display_data(screen)
    pygame.display.update()

pygame.quit()
