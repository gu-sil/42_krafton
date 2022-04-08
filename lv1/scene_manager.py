from actor import Actor
from main_character import MainCharacter
from logger import Logger
import os

# Scene에 있는 액터 데이터를 이용해
# 스타트, 업데이트, 렌더링 등 수행
class SceneManager:
	def __init__(self, w : int, h : int, scene_name : str):
		self._width = w
		self._height = h
		self._actors = []
		self.load_scene_file(scene_name)
		self._logger = Logger()

	def start_all_actors(self):
		for actor in self._actors:
			actor.start()

	def update_all_actors(self):
		for actor in self._actors:
			actor.update()

	def render(self):
		# clear terminal
		os.system('cls' if os.name == 'nt' else 'clear')
		# make render image
		render_image = []
		for i in range(self._height):
			render_image.append(['.'] * self._width)
		# render actors in the scene to the image
		for actor in self._actors:
			render_image[actor._y][actor._x] = actor._ch
		# print logs
		self._logger.print_all_logs()
		# print image
		for i in reversed(range(self._height)):
			print(''.join(render_image[i]))

	def add_movement_input(self, dx : int, dy : int):
		if self._check_valid_pos(self._main_character._x + dx, self._main_character._y + dy):
			self._main_character._x += dx
			self._main_character._y += dy
			# write log
			self._logger.clean_log()
			self._logger.add_log("Move (" + str(dx) + ", " + str(dy) + ")")

	def _check_valid_pos(self, x, y):
		if x < 0 or x >= self._width:
			return False
		elif y < 0 or y >= self._height:
			return False
		else:
			return True

	def load_scene_file(self, scene_name):
		with open(scene_name) as scene:
			for line in scene:
				line = line.strip()
				split_line = line.split()
				if split_line[0] == 'a':
					self._actors.append(Actor(int(split_line[1]), \
											int(split_line[2]), \
											split_line[3]))
				elif split_line[0] == 'mc':
					self._actors.append(MainCharacter(int(split_line[1]),\
													int(split_line[2]),\
													split_line[3]))
					self._main_character = self._actors[len(self._actors) - 1]
		print("Scene", scene_name, "is loaded.")
		for actor in self._actors:
			print(actor._x, actor._y, actor._ch)
