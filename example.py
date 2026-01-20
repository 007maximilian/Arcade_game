import random
from dataclasses import dataclass

import arcade
from arcade.particles import FadeParticle, Emitter, EmitBurst, EmitInterval, EmitMaintainCount
from pyglet.graphics import Batch

# Окно и цвета
W, H = 1000, 650
TITLE = "Arcade Particles — Playground"

# Сделаем набор текстур прямо в рантайме (быстро и дёшево)
SPARK_TEX = [
    arcade.make_soft_circle_texture(8, arcade.color.PASTEL_YELLOW),
    arcade.make_soft_circle_texture(8, arcade.color.PEACH),
    arcade.make_soft_circle_texture(8, arcade.color.BABY_BLUE),
    arcade.make_soft_circle_texture(8, arcade.color.ELECTRIC_CRIMSON),
]
SMOKE_TEX = arcade.make_soft_circle_texture(20, arcade.color.LIGHT_GRAY, 255, 80)
PUFF_TEX = arcade.make_soft_circle_texture(12, arcade.color.WHITE, 255, 50)


# Мутаторы (каждый кадр чуть-чуть меняют частицу)
def gravity_drag(p):  # Для искр: чуть вниз и затухание скорости
    p.change_y += -0.03
    p.change_x *= 0.92
    p.change_y *= 0.92


def smoke_mutator(p):  # Дым раздувается и плавно исчезает
    p.scale_x *= 1.02
    p.scale_y *= 1.02
    p.alpha = max(0, p.alpha - 2)


# Фабрики эмиттеров (возвращают готовый Emitter)
def make_explosion(x, y, count=80):
    # Разовый взрыв с искрами во все стороны
    return Emitter(
        center_xy=(x, y),
        emit_controller=EmitBurst(count),
        particle_factory=lambda e: FadeParticle(
            filename_or_texture=random.choice(SPARK_TEX),
            change_xy=arcade.math.rand_in_circle((0.0, 0.0), 9.0),
            lifetime=random.uniform(0.5, 1.1),
            start_alpha=255, end_alpha=0,
            scale=random.uniform(0.35, 0.6),
            mutation_callback=gravity_drag,
        ),
    )


def make_ring(x, y, count=40, radius=5.0):
    # Кольцо искр (векторы направлены по окружности)
    return Emitter(
        center_xy=(x, y),
        emit_controller=EmitBurst(count),
        particle_factory=lambda e: FadeParticle(
            filename_or_texture=random.choice(SPARK_TEX),
            change_xy=arcade.math.rand_on_circle((0.0, 0.0), radius),
            lifetime=random.uniform(0.8, 1.4),
            start_alpha=255, end_alpha=0,
            scale=random.uniform(0.4, 0.7),
            mutation_callback=gravity_drag,
        ),
    )


def make_fountain(x, y):
    # Фонтанчик: равномерный «дождик» вверх, бесконечно
    return Emitter(
        center_xy=(x, y),
        emit_controller=EmitInterval(0.02),  # Непрерывный поток
        particle_factory=lambda e: FadeParticle(
            filename_or_texture=PUFF_TEX,
            change_xy=(random.uniform(-0.8, 0.8), random.uniform(4.0, 6.0)),
            lifetime=random.uniform(0.8, 1.6),
            start_alpha=240, end_alpha=0,
            scale=random.uniform(0.4, 0.8),
            mutation_callback=gravity_drag,
        ),
    )


def make_smoke_puff(x, y):
    # Короткий «пых» дыма: медленно плывёт и распухает
    return Emitter(
        center_xy=(x, y),
        emit_controller=EmitBurst(12),
        particle_factory=lambda e: FadeParticle(
            filename_or_texture=SMOKE_TEX,
            change_xy=arcade.math.rand_in_circle((0.0, 0.0), 0.6),
            lifetime=random.uniform(1.5, 2.5),
            start_alpha=200, end_alpha=0,
            scale=random.uniform(0.6, 0.9),
            mutation_callback=smoke_mutator,
        ),
    )


def make_trail(attached_sprite, maintain=60):
    # «След за объектом»: поддерживаем постоянное число частиц
    emit = Emitter(
        center_xy=(attached_sprite.center_x - 18, attached_sprite.center_y),
        emit_controller=EmitMaintainCount(maintain),
        particle_factory=lambda e: FadeParticle(
            filename_or_texture=random.choice(SPARK_TEX),
            change_xy=arcade.math.rand_in_circle((0.0, 0.0), 1.6),
            lifetime=random.uniform(0.35, 0.6),
            start_alpha=220, end_alpha=0,
            scale=random.uniform(0.25, 0.4),
        ),
    )
    # Хитрость: каждое обновление будем прижимать центр к спрайту (см. ниже)
    emit._attached = attached_sprite
    return emit


# Движение игрока можно реализовать через датакласс для хранения состояния ввода
@dataclass
class InputState:
    left: bool = False
    right: bool = False
    up: bool = False
    down: bool = False


class Playground(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.DARK_SLATE_GRAY
        self.emitters = []
        self.fountain = None
        self.trail = None

        # «Игрок»: просто квадратик
        self.player = arcade.SpriteSolidColor(36, 36, arcade.color.AZURE)
        self.player.center_x, self.player.center_y = W // 2, H // 2
        self.input = InputState()
        self.player_sprites = arcade.SpriteList()
        self.player_sprites.append(self.player)

        # Подсказки
        self.batch = Batch()

        text = [
            "ЛКМ — взрыв, ПКМ — кольцо, SHIFT + ЛКМ — фонтан",
            "T — след за игроком, C — очистить",
            f"Эмиттеров: {len(self.emitters)}",
        ]
        self.text = []
        for i, line in enumerate(text):
            self.text.append(arcade.Text(line, 10, H - 20 - i * 20,
                                         arcade.color.WHITE, 13,
                                         batch=self.batch))

    # Ввод
    def on_key_press(self, key, mod):
        if key in (arcade.key.A, arcade.key.LEFT):  self.input.left = True
        if key in (arcade.key.D, arcade.key.RIGHT): self.input.right = True
        if key in (arcade.key.W, arcade.key.UP):    self.input.up = True
        if key in (arcade.key.S, arcade.key.DOWN):  self.input.down = True

        if key == arcade.key.T:
            if self.trail:
                self.emitters.remove(self.trail)
                self.trail = None
            else:
                self.trail = make_trail(self.player)
                self.emitters.append(self.trail)

        if key == arcade.key.C:
            self.emitters.clear()
            self.fountain = None
            self.trail = None

    def on_key_release(self, key, mod):
        if key in (arcade.key.A, arcade.key.LEFT):  self.input.left = False
        if key in (arcade.key.D, arcade.key.RIGHT): self.input.right = False
        if key in (arcade.key.W, arcade.key.UP):    self.input.up = False
        if key in (arcade.key.S, arcade.key.DOWN):  self.input.down = False

    def on_mouse_press(self, x, y, button, mod):
        if button == arcade.MOUSE_BUTTON_LEFT and not (mod & arcade.key.MOD_SHIFT):
            self.emitters.append(make_explosion(x, y))
            self.emitters.append(make_smoke_puff(x, y))
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            self.emitters.append(make_ring(x, y))
        elif button == arcade.MOUSE_BUTTON_LEFT and (mod & arcade.key.MOD_SHIFT):
            # Переключаем фонтан в этой точке
            if self.fountain:
                self.emitters.remove(self.fountain)
                self.fountain = None
            else:
                self.fountain = make_fountain(x, y)
                self.emitters.append(self.fountain)

    # Логика
    def on_update(self, dt):
        # Движение игрока
        v = 280 * dt
        if self.input.left:  self.player.center_x -= v
        if self.input.right: self.player.center_x += v
        if self.input.up:    self.player.center_y += v
        if self.input.down:  self.player.center_y -= v
        self.player.center_x = max(18, min(W - 18, int(self.player.center_x)))
        self.player.center_y = max(18, min(H - 18, int(self.player.center_y)))

        # Подкручиваем центр «следа» к игроку
        if self.trail:
            self.trail.center_x = self.player.center_x
            self.trail.center_y = self.player.center_y

        # Обновляем эмиттеры и чистим «умершие»
        emitters_copy = self.emitters.copy()  # Защищаемся от мутаций списка
        for e in emitters_copy:
            e.update(dt)
        for e in emitters_copy:
            if e.can_reap():  # Готов к уборке?
                self.emitters.remove(e)

    # Рендер
    def on_draw(self):
        self.clear()
        for e in self.emitters:
            e.draw()
        self.player_sprites.draw()

        self.batch.draw()


def main():
    window = arcade.Window(W, H, TITLE)
    window.show_view(Playground())
    arcade.run()


if __name__ == "__main__":
    main()