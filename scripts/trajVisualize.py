from ase.io import read, write
from ase import Atoms
import matplotlib.pyplot as plt
import imageio
from PIL import Image
import sys
import os


def traj_to_pngs(vasprun_file: str = 'vasprun.xml', view='-90x, -90y, 0z', output: str = 'tmp1'):
    # use the vasprun.xml file to get the trajectory
    traj = read(vasprun_file, ':')

    # write the images to temporary files in the current directory tmp1_{i}.png
    for i, atoms in enumerate(traj):
        write(f'{output}_{i}.png', atoms, rotation=view)

    return len(traj)


def pngs_to_gif(pngs: list, gif_name: str = 'traj.gif'):
    # use imageio to create a gif from the images
    images = []
    for png in pngs:
        images.append(imageio.imread(png))
    # make the background transparent
    images = [Image.fromarray(image).convert('RGBA') for image in images]
    imageio.mimsave(gif_name, images, fps=5)


def plot_ionic_convergence(vasprun_file: str = 'vasprun.xml'):
    # use the vasprun.xml file to get the trajectory
    traj = read(vasprun_file, ':')

    # get the energies
    energies = [atoms.get_potential_energy() for atoms in traj]

    # ionic steps
    ionic_steps = [i for i in range(len(energies))]

    # plot the energies
    plt.plot(energies, 'o-')
    plt.title('Ionic convergence')
    plt.xlabel('Step')
    plt.ylabel('energy (eV)')

    # put an orange circle at each step on the line plot
    for i, j in zip(ionic_steps, energies):
        plt.plot(i, j, 'o', color='orange')
        # save the image
        plt.savefig(f'tmp2_{i}.png')


def stitch_images(png_structures: list[str], png_energies: list[str], png_top_views: list[str]):
    # get the images
    structures = [Image.open(png) for png in png_structures]
    top_views = [Image.open(png) for png in png_top_views]
    energies = [Image.open(png) for png in png_energies]

    # stitch the images together
    stitched = []
    for i in range(len(structures)):
        stitched.append(Image.new(
            'RGB', (structures[i].width + energies[i].width, structures[i].height)))
        stitched[i].paste(structures[i], (0, 0))
        stitched[i].paste(energies[i], (structures[i].width, 0))
        # add top views to the bottom right corner
        stitched[i].paste(top_views[i], (structures[i].width + 1,
                          structures[i].height - top_views[i].height))

    # save the images
    for i, image in enumerate(stitched):
        image.save(f'tmp3_{i}.png')

    return len(stitched)


if __name__ == '__main__':
    # get the pngs from the trajectory
    directory = sys.argv[1]
    length = traj_to_pngs(f'{directory}/vasprun.xml')

    structure_pngs = [f'tmp1_{i}.png' for i in range(length)]
    plot_ionic_convergence(f'{directory}/vasprun.xml')

    energy_pngs = [f'tmp2_{i}.png' for i in range(length)]

    lenght_2 = traj_to_pngs(f'{directory}/vasprun.xml',
                            view='0x, 0y, 0z', output='top')

    top_view_pngs = [f'top_{i}.png' for i in range(lenght_2)]

    stitched_pngs = stitch_images(structure_pngs, energy_pngs, top_view_pngs)

    stitched_pngs = [f'tmp3_{i}.png' for i in range(stitched_pngs)]

    # make the gif
    pngs_to_gif(stitched_pngs, f'{directory}/traj.gif')

    # remove the temporary files
    for png in structure_pngs + energy_pngs + top_view_pngs + stitched_pngs:
        os.remove(png)
