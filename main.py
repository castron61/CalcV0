import tkinter as tk
    from tkinter import ttk, colorchooser
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from calculator import BeamCalculator

    class App:
      def __init__(self, root):
        self.root = root
        self.root.title("3D GUI Application")
        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()
        self.background_color = (1.0, 1.0, 1.0, 1.0)  # White background
        self.camera_distance = -5.0
        self.rotation_angle = 0.0

        self.calc = BeamCalculator()

        self.create_menu()
        self.setup_canvas()

      def create_menu(self):
        menu_bar = tk.Menu(self.root)
        settings_menu = tk.Menu(menu_bar, tearoff=0)
        settings_menu.add_command(label="Change Background Color", command=self.change_background_color)
        menu_bar.add_cascade(label="Settings", menu=settings_menu)
        self.root.config(menu=menu_bar)

      def change_background_color(self):
        color_code = colorchooser.askcolor(title="Choose a background color")[1]
        if color_code:
          r, g, b = map(int, color_code[1:].split(''))
          self.background_color = (r / 255.0, g / 255.0, b / 255.0, 1.0)

      def setup_canvas(self):
        self.canvas.bind("<Button-3>", self.on_mouse_click)
        self.canvas.bind("<B1-Motion>", self.on_pan)
        self.canvas.bind("<Control-L>", self.on_rotate_left)
        self.canvas.bind("<Control-R>", self.on_rotate_right)
        self.canvas.bind("<Control-Up>", self.on_zoom_in)
        self.canvas.bind("<Control-Down>", self.on_zoom_out)

      def on_mouse_click(self, event):
        pass

      def on_pan(self, event):
        pass

      def on_rotate_left(self, event):
        self.rotation_angle += 1.0
        self.draw()

      def on_rotate_right(self, event):
        self.rotation_angle -= 1.0
        self.draw()

      def on_zoom_in(self, event):
        self.camera_distance -= 0.5
        self.draw()

      def on_zoom_out(self, event):
        self.camera_distance += 0.5
        self.draw()

      def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluPerspective(45, (self.canvas.winfo_width() / self.canvas.winfo_height()), 0.1, 50.0)
        glTranslatef(0.0, 0.0, self.camera_distance)
        glRotatef(self.rotation_angle, 0.0, 1.0, 0.0)

        # Draw your 3D objects here
        glBegin(GL_QUADS)
        glColor4fv((0.5, 0.5, 0.5, 1.0))
        glVertex3fv((-1.0, -1.0, -1.0))
        glVertex3fv((1.0, -1.0, -1.0))
        glVertex3fv((1.0, 1.0, -1.0))
        glVertex3fv((-1.0, 1.0, -1.0))
        glEnd()

        self.canvas.after(16, self.draw)

    if __name__ == "__main__":
      root = tk.Tk()
      app = App(root)
      root.mainloop()
