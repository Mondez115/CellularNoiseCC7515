import glfw

if __name__ == "__main__":

    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 800
    height = 800

    window = glfw.create_window(width, height, "Test", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
       
       glfw.poll_events()

       glfw.swap_buffers(window)


    glfw.terminate()

