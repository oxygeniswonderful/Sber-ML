import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.colors import LogNorm
import numpy as np
from itertools import zip_longest

class TrajectoryAnimation(animation.FuncAnimation):
    
    def __init__(self, *paths, labels=[], skip_samples=500, fig=None, ax=None, frames=None, 
                 interval=60, repeat_delay=5, blit=True, **kwargs):

        if fig is None:
            if ax is None:
                fig, ax = plt.subplots()
            else:
                fig = ax.get_figure()
        else:
            if ax is None:
                ax = fig.gca()

        self.fig = fig
        self.ax = ax
        
        self.paths = paths

        if frames is None:
            frames = max(path.shape[1] for path in paths)
  
        self.lines = [ax.plot([], [], label=label, lw=2)[0] 
                      for _, label in zip_longest(paths, labels)]
        self.points = [ax.plot([], [], '--o', color=line.get_color())[0] 
                       for line in self.lines]

        self.skip_samples = skip_samples

        super(TrajectoryAnimation, self).__init__(fig, self.animate, init_func=self.init_anim,
                                                  frames=frames, interval=interval, blit=blit,
                                                  repeat_delay=repeat_delay, **kwargs)

    def init_anim(self):
        for line, point in zip(self.lines, self.points):
            line.set_data([], [])
            point.set_data([], [])
        return self.lines + self.points

    def animate(self, i):
        for line, point, path in zip(self.lines, self.points, self.paths):
            line.set_data(*path[::,:i*self.skip_samples])
            point.set_data(*path[::,(i-1)*self.skip_samples:i*self.skip_samples])
        return self.lines + self.points
    
    
def prepare_2d_countor_plot(x,y,z, x_lim, y_lim, minimum):
    minima = minimum.reshape(-1, 1)
    xmin, xmax = x_lim
    ymin, ymax = y_lim
    
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.contour(x, y, z, levels=np.logspace(0, 5, 35), norm=LogNorm(), cmap=plt.cm.jet)
    ax.plot(*minima, 'r*', markersize=18)

    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')

    ax.set_xlim((xmin, xmax))
    ax.set_ylim((ymin, ymax))

    return ax
    

def prepare_beale_3d_countor_plot(x,y,z, f):
    minima = np.array([3., .5]).reshape(-1, 1)
    xmin, xmax = -4.5, 4.5
    ymin, ymax = -4.5, 4.5
    
    fig = plt.figure(figsize=(10, 6))
    ax = plt.axes(projection='3d', elev=30, azim=-50)

    ax.plot_surface(x, y, z, norm=LogNorm(), rstride=1, cstride=1, 
                    edgecolor='none', alpha=.8, cmap=plt.cm.jet)
    ax.plot(*minima, f(*minima), 'r*', markersize=10)

    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    ax.set_zlabel('$z$')

    ax.set_xlim((xmin, xmax))
    ax.set_ylim((ymin, ymax))

    return ax