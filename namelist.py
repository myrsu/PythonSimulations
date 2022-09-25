from math import pi, sqrt
import numpy as np

l0 = 2. * np.pi             # laser wavelength [in code units]
t0 = l0                     # optical cycle
Lsim = [140.*l0]            # length of the simulation
resx = 768                  # nb of cells in one laser wavelength
rest = resx                 # nb of timesteps in one optical cycle 
n_particles = 50
n_of_patches = 128
w = 0.1
conc = 0.2
l_step = 30
Tsim = 200*t0               # duration of the simulation
A = 20.                     # a0

Main(
    geometry = "1Dcartesian",
    
    interpolation_order = 2 ,
    
    cell_length = [l0/resx],
    grid_length  = Lsim,
    
    number_of_patches = [n_of_patches], 
    solve_poisson = False,
    poisson_max_iteration = 2e5,
    poisson_max_error = 1e-35,
    solve_relativistic_poisson = True,
    relativistic_poisson_max_iteration = 2e5,
    relativistic_poisson_max_error = 1e-40,
    maxwell_solver = 'M4',
    timestep = t0/rest,
    simulation_time = Tsim,
     
    EM_boundary_conditions = [
        ['silver-muller']
    ],
    
    random_seed = 0
)

# Laser
LaserPlanar1D(
    box_side         = "xmin",
    a0               = A,
    omega            = 1.,
    polarization_phi = 0.,
    ellipticity      = 1., #The polarization ellipticity: 0 for linear and 1, -1 for circular.
    time_envelope    = tgaussian(start=0.0, duration=l_step*l0, fwhm=2*l0, center=None, order=2)
)

#e_wall
Species(
    name      = "electron",
    position_initialization = "random",
    momentum_initialization = "cold",
    regular_number = [],
    particles_per_cell = n_particles,
    mass = 1.,
    atomic_number = None,
    number_density = trapezoidal(max = conc, xvacuum = 125*l0, xplateau = w * l0, xslope1=0.0, xslope2=0.0),
    charge = -1.,
    mean_velocity = [-0.99999, 0., 0.],
    temperature = [0],
    boundary_conditions = [
        ["remove", "remove"],
    ],
    is_test = False,
    pusher = "boris",
)

CurrentFilter()

# DiagScalar(
#     every = rest
# )

DiagFields(
    every = rest,
    fields = ['Rho_electron', 'Ey', 'Ez']
)

DiagProbe(
    every    = 1,
    origin   = [5*l0],
    fields = ['Ey','Ez','By','Bz'],
)

DiagProbe(
    every    = 1,
    origin   = [135*l0],
    fields = ['Ey','Ez','By','Bz'],
)
