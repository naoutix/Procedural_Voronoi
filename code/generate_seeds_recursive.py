import numpy
import matplotlib.pyplot as plt


def sample_new_point(origin_square, length_halfsquare, subidx):
    dx, dy = subidx % 2, subidx // 2
    offset = length_halfsquare * numpy.array([dx, dy], dtype=float)
    random_offset = numpy.array([numpy.random.random(), numpy.random.random()])
    return origin_square + random_offset * length_halfsquare + offset


def subdivide_square(origin_square, length_square, seeds, density_func):
    length_halfsquare = 0.5 * length_square
    rho = density_func(origin_square + length_halfsquare)
    target_seeds = (length_square ** 2) * rho
    if target_seeds <= 4:
        # 1st case: the cell is a leaf
        shuffled_idx = numpy.random.permutation(4)
        min_samples = int(numpy.floor(target_seeds))
        proba_last = target_seeds - min_samples
        for i in range(min_samples):
            seeds.append(sample_new_point(origin_square, length_halfsquare, shuffled_idx[i]))
        if numpy.random.random() <= proba_last and min_samples < 4:
            seeds.append(sample_new_point(origin_square, length_halfsquare, shuffled_idx[min_samples]))
    else:
        # 2nd case: recursive call
        for delta in numpy.ndindex(2, 2):
            offset = numpy.array(delta, dtype=float)
            origin_subsquare = origin_square + offset * length_halfsquare
            subdivide_square(origin_subsquare, length_halfsquare, seeds, density_func)


def plot_seeds(seeds, extent):
    seeds_x = [s[0] for s in seeds]
    seeds_y = [s[1] for s in seeds]
    plt.scatter(seeds_x, seeds_y, s=0.5)
    plt.xlim([0, extent[0]])
    plt.ylim([0, extent[1]])
    plt.axes().set_aspect('equal')
    plt.show()


def generate_seeds(coarse_level_length, extent):
    def density_func(point):
        # grading in x direction
        seed_density_factor = 2000
        return (point[0] / extent[0]) * seed_density_factor  # seeds / mm^2

    numpy.random.seed(1)
    seeds = []
    for origin_x in numpy.arange(0.0, extent[0], coarse_level_length):
        for origin_y in numpy.arange(0.0, extent[1], coarse_level_length):
            origin_square_coarse = numpy.array([origin_x, origin_y], dtype=float)
            subdivide_square(origin_square_coarse, coarse_level_length, seeds, density_func)

    return seeds


if __name__ == "__main__":
    coarse_level_length = 4.0  # (mm)
    extent = numpy.array([8.0, 2.0], dtype=float)  # (mm)
    seeds = generate_seeds(coarse_level_length, extent)
    plot_seeds(seeds, extent)
