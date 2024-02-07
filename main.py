import pygame

from pygame.locals import *

import sys


# -----------

# Constants

SCREEN_WIDTH = 1000

SCREEN_HEIGHT = 675

sea_level = 80

submarine_image_pos_x = 500

submarine_image_pos_yLim = 500

submarine_image_pos_y_init = sea_level

# Gravity constant

g = 9.8

# Fluid density  1000 m^3/kg for water

p = 1000

# Robot total volume

v = 1

# Delta time. It depends on CPU clock frequency and computational complexity

dt = 1

# Friction constant

b = 250

# Buoyancy

e = - (p * g * v)


# ------------------------------

# Classes and Functions

# ------------------------------


class Reservoir:

   def __init__(self, actual_level, valve_flow, max_capacity, fluid_to_pump):

       self.actual_level = actual_level

       self.valve_flow = valve_flow

       self.max_capacity = max_capacity

       self.fluid_to_pump = fluid_to_pump


   def pumping_air_water(self, fluid_to_pump):

       if fluid_to_pump == 'air':

           if self.actual_level > 0:

               self.actual_level = self.actual_level - self.valve_flow

           else:

               self.actual_level = 0

       if fluid_to_pump == 'water':

           if self.actual_level < self.max_capacity:

               self.actual_level = self.actual_level + self.valve_flow

           else:

               self.actual_level = self.max_capacity



class Submarine:

   def __init__(self, tank, mass, actual_velocity_x, actual_velocity_y, pos_x, pos_y):

       self.pos_x = pos_x

       self.pos_y = pos_y

       self.mass = mass

       self.actual_velocity_x = actual_velocity_x

       self.actual_velocity_y = actual_velocity_y

       self.tank = tank


   def calculate_mass(self):

       self.mass = self.tank.actual_level

   def calculate_velocity_x(self):

       # La fuerza aplicada en el eje x podría ser un valor constante

       fx = 100

       self.actual_velocity_x = dt * ((fx / self.mass) - ((b * self.actual_velocity_x) / self.mass)) + self.actual_velocity_x

   def calculate_velocity_y(self):

       self.actual_velocity_y = dt * ((e / self.mass) + g - ((b * self.actual_velocity_y) / self.mass)) + self.actual_velocity_y


   def calculate_position_x(self):

       self.pos_x = self.pos_x + self.actual_velocity_x

       # -----------------------------------------------------------------

       # Verify that the actual position isn´t greater than the screen edge

       # -----------------------------------------------------------------

       if self.pos_x > SCREEN_WIDTH:

           self.pos_x = SCREEN_WIDTH

       if  self.pos_x < 0:

           self.pos_x = 0

   def calculate_position_y(self):

       self.pos_y = self.pos_y + self.actual_velocity_y

       # -----------------------------------------------------------------

       # Verify that the actual position isn´t greater than the screen edge

       # -----------------------------------------------------------------

       if self.pos_y > submarine_image_pos_yLim:

           self.pos_y = submarine_image_pos_yLim

       if  self.pos_y < sea_level:

           self.pos_y = sea_level

       # --------------------------------------------

       return self.pos_x, self.pos_y


# ------------------------------

# Main function

# ------------------------------

def main():

   pygame.init()

   tank1 = Reservoir(1005, 2, 50000, 'air')

   submarine1 = Submarine(tank1, 2, 2, 2, 150, submarine_image_pos_y_init)


   # --------------------------------------------

   # Creation of the window and assigning a title

   # --------------------------------------------

   screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

   pygame.display.set_caption("Submarine game")

   # -----------------------------------------

   # Load images (creation of Surface objects)

   # -----------------------------------------

   background_image = pygame.image.load("mar.jpg").convert()

   # Some image formats needs alpha conversion

   submarine_image = pygame.image.load("sub.jpg").convert_alpha()

   # --------------------------------------------

   # The blit method place images onto screen

   # We specify the position of the 'Surface' on the window

   # --------------------------------------------

   screen.blit(submarine_image, (submarine_image_pos_x, submarine_image_pos_y_init))

   screen.blit(background_image, (0, 0))

   # --------------------------------------------

   # Displaying changes on the screen

   # --------------------------------------------

   pygame.display.flip()


   # Main loop

   while True:

       # -------------------------------------------------------------------------------------

       # Increases the distance measured from sea level, due to the permanent action of gravity

       # -------------------------------------------------------------------------------------

       submarine1.calculate_velocity_x()

       submarine1.calculate_velocity_y()

       submarine1.calculate_position_x()

       submarine1.calculate_position_y()

       print(submarine1.actual_velocity_x, submarine1.actual_velocity_y)



       # place Images onto screen

       # --------------------------------------------

       screen.blit(background_image, (0, 0))

       screen.blit(submarine_image, (submarine1.pos_x, submarine1.pos_y))

       # --------------------------------------------

       # Re-draw all elements

       # --------------------------------------------

       pygame.display.flip()

       # --------------------------------------------

       # Possible mouse and keyboard inputs

       # --------------------------------------------

       for event in pygame.event.get():

           if event.type == pygame.QUIT:

               sys.exit()

           elif event.type == pygame.KEYDOWN:

               if event.key == K_UP:

                   tank1.pumping_air_water('air')

               elif event.key == K_DOWN:

                   tank1.pumping_air_water('water')

               elif event.key == K_LEFT:

                   # Añadir una fuerza negativa en el eje x para simular el movimiento a la izquierda

                   fx = -100

               elif event.key == K_RIGHT:

                   # Añadir una fuerza positiva en el eje x para simular el movimiento a la derecha

                   fx = 100

               elif event.key == K_UP:

                   # Añadir una fuerza negativa en el eje y para simular el movimiento hacia arriba

                   fy = -100

               elif event.key == K_DOWN:

                   # Añadir una fuerza positiva en el eje y para simular el movimiento hacia abajo

                   fy = 100

       submarine1.calculate_mass()


if __name__ == "__main__":

   main()