# ACCESS-ESM with PAYU

## Understanding PAYU

PAYU was designed to help users of the NCI system run climate models.
It was initially created for MOM, but has been adapted for other models,
including coupled ones.

The aim of PAYU is to make it easy and intuitive to configure and run the models.

PAYU knows certain models and how to run them. Adding more models needs additions to the PAYU sources.
This will not be part of this document.

### Terms

To understand PAYU, it helps to distinguish certain terms:

-   The **Laboratory** is a directory where all parts of the model are kept.
    It is typically in the user's short directory, usually at `/short/$PROJECT/$USER/<MODEL>`
-   The **Control Directory** is the directory where the model configuration is
    kept and where from where the model is run.
-   The **work** directory is where the model will actually be run.
    It is typically a subdirectory of the Laboratory.
    Submodels will have their own subdirectories in the work directory, named
    after their name in the master configuration file.
-   The **archive** directory is where payu pushes all output files after each run.

The **work** and **archive** directories will be automatically created by payu, the
other two you will have to create.

### The master configuration file

In the Control Directory, the file `config.yaml` is the master control file.
Examples of what is configured in this file are:

-   The actual model to run.
-   Where to find the model binaries and configurations
-   What resources to request from the scheduling system (PBS)
-   Links to the laboratory
-   Start date and run length per submission pf the model

The model configuration files are typically in subdirectories of the Control Directory,
the location of which is referenced in the master control file.
Since the models itself do need different ways to set up the model, the contents of these subdirectories will differ between different models.

## Understanding ACCESS-ESM

ACCESS (Australian Community Climate and Earth System Simulator) is a Coupled Climate Model.

The ESM 1.5 subversion of ACCESS specifically contains these models:

| Component  | Model      | Version |
| ---------- | ---------- | ------- |
| Atmosphere | UM-HG3     | 7.3     |
| Ocean      | MOM        | 4       |
| Sea Ice    | CICE       | 4.1     |
| Coupler    | OASIS-MCT  | 3.5     |

Pre-compiled executables for these models are available on raijin at
`/short/public/access-esm/payu/bin/csiro/`.

## Setting up ACCESS-ESM with PAYU

### The pre-conditions

On `raijin`, first make sure that you have access to our modules.
This can most easily been done by adding the line

    module use /g/data3/hh5/public/modules

to your `~/.bashrc`, then logging back in. Then all you have to do is

    $ module load payu

to load the payu module. We also recommend you load a more recent version of `git` with

    $ module load git

as payu will use git to keep track of all configuration changes automatically.

### Setting up the control directory

Create a directory in your home directory to keep all the Control Directories you might want.

    $ mkdir ~/ACCESS-ESM
    $ cd ~/ACCESS-ESM

Then clone the most recent version of the ACCESS-ESM control directory:

    $ git clone https://github.com/coecms/esm-pre-industrial pre-industrial
    $ cd pre-industrial

(Note: Currently we only have the pre-industrial model set up, other versions will follow later.)

### Setting up the Master Configuration file.

Open the `config.yaml` file with your preferred text editor.

Let's have a closer look at the parts:

    jobname: pre-industrial
    queue: normal
    walltime: 20:00:00

These are settings for the PBS system. Name, walltime and queue to use.

    # note: if laboratory is relative path, it is relative to /short/$PROJECT/$USER
    laboratory: access-esm

The location of the laboratory. At this point, payu can not expand shell environment variables (it's in our TO-DO), so as a work-around, if you use relative paths, it will be relative to your default short directory.

In this default configuration, it will be in `/short/$PROJECT/$USER/access-esm`.
But you can also hard-code the full path, if you want it somewhere different.

    model: access

The main model. This mainly tells PAYU which driver to use. PAYU knows that **access** is a coupled model, so it will look for separate configurations of the submodels, which is the next item of the configuration file:

    submodels:
        - name: atmosphere
          model: um
          ncpus: 192
          exe: /short/public/access-esm/payu/bin/csiro/um_hg3.exe-20190129_15
          input:
            - /short/public/access-esm/payu/input/pre-industrial/atmosphere

        - name: ocean
          model: mom
          ncpus: 84
          exe: /short/public/access-esm/payu/bin/coe/fms_ACCESS-CM.x
          input:
            - /short/public/access-esm/payu/input/common/ocean
            - /short/public/access-esm/payu/input/pre-industrial/ocean

        - name: ice
          model: cice
          ncpus: 12
          exe: /short/public/access-esm/payu/bin/csiro/cice4.1_access-mct-12p-20180108
          input:
            - /short/public/access-esm/payu/input/common/ice

        - name: coupler
          model: oasis
          ncpus: 0
          input:
            - /short/public/access-esm/payu/input/common/coupler

This is probably the meatiest part of the configuration, so let's look at it in more detail.

Each submodel has
- a **name**
- the **model** to know which driver to use
- the number of CPUs that this model should receive (**ncpus**)
- the location of the executable to use (**exe**)
- one or more locations for the **input** files.

The **name** is more than a useful reminder of what the model is.
PAYU expects this submodel's configuration files in a subdirectory with that name.

    collate:
       exe: /short/public/access-esm/payu/bin/mppnccombine
       restart: true
       mem: 4GB

Ask Aidan

    restart: /short/public/access-esm/payu/restart/pre-industrial

Ask Aidan

    calendar:
        start:
            year: 101
            month: 1
            days: 1

        runtime:
            years: 1
            months: 0
            days: 0

Here is the start date, and the runtime **per run**.
The total time you want to model is `runtime` * `number of runs`

    runspersub: 5

This `runspersub` feature is a nifty tool to allow you to bundle several runs into a single submission for the PBS queue.

Let's have an example: Say you told payu to make 7 runs with the above setting.
Each run would have a runtime of 1 year. So in the first submission it would run the model 5 times, to model years 101 through 105 respectively.

Then it would automatically resubmit another pbs job to model years 106 and 107, and then end.

### Setting up the Atmosphere Submodel

The **name** in `config.yaml` for the atmosphere submodel is "atmosphere", so the configuration of the UM will be in the `atmosphere` subdirectory.

    $ ls atmosphere/
    CNTLALL   SIZES      __pycache__  ftxx       ihist          prefix.CNTLATM
    CONTCNTL  STASHC     cable.nml    ftxx.new   input_atm.nml  prefix.CNTLGEN
    INITHIS   UAFILES_A  errflag      ftxx.vars  namelists      prefix.PRESM_A
    PPCNTL    UAFLDS_A   exstat       hnlist     parexe         um_env.py

There are many configuration files, but I want to note the `um_env.py`.
This file is used to set environment variables for the UM.
The UM driver of PAYU will look for this file and execute it.

### Setting up the Ocean Submodel

The **name** in `config.yaml` for the ocean submodel is "ocean", so the configuration
of MOM will be in the `ocean` subdirectory.

    $ ls ocean
    data_table  diag_table  field_table  input.nml


### Setting up the Ocean Submodel

The **name** in `config.yaml` for the ice submodel is "ice", so the configuration
of CICE will be in the `ice` subdirectory.

    $ ls ice/
    cice_in.nml  input_ice.nml

## Running the Model

If you have set up the modules system to use the `/g/data3/hh5/public/modules` folder, a simple `module load payu` should give you access to the payu system.

From the control directory, type

    $ payu setup

This will prepare a the model run based on the configuration of the experiment.
It will setup `work` and `archive` directories and link to them from within the
configuration directory.
You don't have to do that, as the run command also sets it up, but it helps to check for errors.

    $ payu sweep

This command removes the `work` directory again, but leaves the `archive`.
You can have it remove the `archive` as well by appending `--hard` to the command.

Finally,

    $ payu run

will submit a single run to the queue.
It will start from the beginning (as indicated by the `start` section in the `config.yaml`) if it has not run before (or if you have run `payu sweep --hard`), otherwise it will continue from the end of the last run.

To automatically submit several runs (and to take advantage of the `runspersub` directive), you use the `-n` option:

    $ payu run -n 7
