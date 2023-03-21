import pygame
import pygame.freetype

import ctypes
user32 = ctypes.WinDLL('user32')
SW_MAXIMISE = 3
SW_SHOWNORMAL = 1

def main():
    pygame.init()
    flags = pygame.RESIZABLE
    screen = pygame.display.set_mode((500, 500), flags)
    hWnd = user32.GetForegroundWindow()
    orgsize = None 

    clock = pygame.time.Clock()

    min = pygame.Rect((0, 16, 32, 32))
    max = pygame.Rect((0, 16, 32, 32))
    close = pygame.Rect((0, 16, 32, 32))

    min.right = screen.get_rect().right - 90
    max.right = screen.get_rect().right - 50
    close.right = screen.get_rect().right - 10

    font = pygame.freetype.SysFont(None, 32)
    font.origin = True
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return
            if e.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((e.w, e.h), flags)
                min.right = screen.get_rect().right - 90
                max.right = screen.get_rect().right - 50
                close.right = screen.get_rect().right - 10
            if e.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if close.collidepoint(pos):
                    return
                if min.collidepoint(pos):
                    pygame.display.iconify()
                if max.collidepoint(pos):
                    if not orgsize:
                        orgsize = screen.get_rect().size
                        user32.ShowWindow(hWnd, SW_MAXIMISE)
                    else:
                        user32.ShowWindow(hWnd, SW_SHOWNORMAL)
                        screen = pygame.display.set_mode(orgsize, flags)
                        orgsize = None

        screen.fill((30, 30, 30))
        pygame.draw.rect(screen, pygame.Color('dodgerblue'), max)
        pygame.draw.rect(screen, pygame.Color('darkorange'), min)
        pygame.draw.rect(screen, pygame.Color('red'), close)
        font.render_to(screen, min.move(7, -10).bottomleft, '_')
        font.render_to(screen, max.move(4, -5).bottomleft, 'O')
        font.render_to(screen, close.move(4, -5).bottomleft, 'X')
        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main()
    pygame.quit()