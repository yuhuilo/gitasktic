"""Oddball Experiment
created by Paul Z. Cheng

Experimental flow:
    (1). Imports and Setups
    (2). Functions
    (3). Excution

** Word on debuging:
    This script is design for minimal variable adjustment in function
    and Excution. All input variable is defined either in configuration file or
    Import and Setup.
"""

## Script Partition ##
""" Each boolean value represent each part of experiment.
If Set true it will run it, this helps with debug.
"""
instruction = True
demo_gui = True
beh = True
eeg = True
debug = False


##############################
### (1).Imports and Setups ###
##############################
## Local import ##
import config                       # expermental variables
import extra    	                # for logging
from list_gene import list_gene
import instruct

## Experimental conditons generation ##
""" Out production of list_gene is a list of list of dictionary
    with formated as followed:

        [[{Trial},{Trial}..][{Trial},{Trial}...]]

    Base level as trials, then bloprintck.
    ** Check list_gene.py for more information.
"""
blocks = list_gene(config)


## Global imports ##
""" Note: Psychopy takes up lots of compuational memory and python name space.
          Thus psychopy import is done after trials generation.
"""
from psychopy import core, visual, gui, monitors, event
from psychopy import parallel
from psychopy.hardware import keyboard

## Run Demographic interface ##
""" Get subject id and other variables.
 Save input variables in "demo" dictionary (demo for "Demographic")
 Note: currently didn't log age or gender, if you want this information
       you need to log it somewhere else.
"""
if demo_gui:
    demo = {"subject":"", "session_id":"", "age":"", "gender":["male", "female"]}
    if not gui.DlgFromDict(demo, order = ["subject", "session_id","age", "gender"]).OK:
        core.quit()

if beh:
    ## Time Configuration ##
    glob_t = core.Clock()         # timming for the whole experiment
    trial_t = core.Clock()         # Trial by Trial timming
    rt_t = core.Clock()            # RT timer

    ## Log Configuration
    """ Custom writing function
     writer.write(trial) writes individual trials with a low latency.
     ** Check extra.py for more information.
    """
    sub_id = "sub-"+str(demo["subject"])
    ses_id = "ses-"+str(demo["session_id"])
    fn_pre = "_".join([sub_id,ses_id])
    log = extra.csv_writer(fn_pre,folder = config.SAVE_FOLDER,
                           column_order = ["cond", "block_num", "trial_num",
                                           "press_glob_time", "stim_on"])

    # debug: get timming after majority setup is finished.
    if debug:
        mm_time = glob_t.getTime()
        print(f"Time it takes to set up : {mm_time}")

    ## Create window ##
    """ Create monitor object, using width and distance to control for control
     size of stimulus in degrees.
    """
    exp_mon = monitors.Monitor("testMonitor", width = config.MON_WIDTH,
                               distance = config.MON_DISTANCE)
    exp_mon.setSizePix(config.MON_SIZE)

    ## Initiate Window
    # using the exp_mon object above, and use degree as units.
    win = visual.Window(monitor = exp_mon, units = "deg", fullscr = True,
                        allowGUI = False, color = "black")

    ## stimulus
    # Setup each present stimulus before experiment began
    # Fixation cross is just the character "+".
    fix = visual.TextStim(win, "+")
    # Stimulus state
    stim_text = visual.TextStim(win, height = config.MESSAGE_HEIGHT,
                                wrapWidth = config.MESSAGE_WIDTH)
    # Initate parallel port
    if eeg:
        ## May need to manually key in the address ##
        #pp = parallel.ParallelPort(address = 0x0378)
        pp = parallel.ParallelPort(address = 0xEFB8)
        pp.setData(0)


###################
## (2).Functions ##
###################
def pp_reset(eeg):
    if eeg:
        pp.setData(0)

def keypress(config):
    """Keypress for the experiment
    Accepts only responds and quit keys set in the configuration file
    and if quit key is accepted, close out the window.
    input:
        config  : config.py
    return
        key     : Key press being pressed
    """
    ## Responds configuration ##
    resp_keys = config.RESPS
    resp_keys += config.KEYS_QUIT

    # add in lowercase
    resp_keys += config.RESPS_L

    # Key press
    key = event.getKeys(keyList = resp_keys)

    # Quit everything if quit key was pressed
    # *Note: In this case is "escape" key
    if config.KEYS_QUIT[0] in key:
        log.flush() # Close the file if quit-key is pressed.
        core.quit()

    return key

def prompt(text = "", keyList=None):
    """Present instruction prompt.
    Shows instruction and returns answer (keypress) and reaction time.
    Defaults is no text and accept all keys.
    input:
        text: text wanted to present.
        keyList: list of keys that it will accept to break out of prompt,
                 if not specified, will accept all keys.

    results:
        Present the screen with prompt given.
    """
    # Draw the TextStims to visual buffer
    # then show it and reset timing immediately (at stimulus onset)
    stim_text.text = text
    stim_text.wrapwidth = True
    stim_text.font = "Arial"
    stim_text.antialias = True

    # Stimulus present
    stim_text.draw()
    time_flip = win.flip()

    # Halt everything and wait for the first responses matching the
    # keys given in the KeyList object
    if keyList:
        keyList += config.KEYS_QUIT

    # There is key time here, may adjust the function to get key time.
    key, time_key = event.waitKeys(keyList = keyList, timeStamped = True)[0]

    # Quit everything if quit key was pressed
    # Note: In this case is "escape" key
    if key in config.KEYS_QUIT:
        log.flush() # Close the file if quit-key is pressed.
        core.quit()

def block_prompt(blocks, bn, config):
    """ Experimental block prompt presentation.
    Funciton initate experimetnal instruction prompts for beginning of each block
    for subject to read.

    Input:
        blocks : A list of list of dictionary with conditions and trial information
        bn     : Python's loop block number i.e 0,1,2,3,4...etc
        config : configuration file with all specific experimental definition

    --------------------------------------------------------
                        Presenting
    --------------------------------------------------------
    upper left  :   Stimulus X or O
    upper right :   Stimulus X or O
    lower left  :   Responds "Press F"
    lower right :   Responds "Press J"
    bottom      :   Press SPACEBAR to begin the next block.
    --------------------------------------------------------
    """
    # General text
    block_break = visual.TextStim(win, text="press SPACE keys to continue...",
                                  pos = (0, -6),antialias = True)
    left_resp_key = visual.TextStim(win, text=f"Press {config.RESPS[0]} ",
                                    font = "Arial", pos = (-5, -1),
                                    antialias = True)
    right_resp_key = visual.TextStim(win, text=f"Press {config.RESPS[1]} ",
                                     font = "Arial", pos = (5, -1),
                                     antialias = True)
    left_resp_stim = visual.TextStim(win, font = "Arial",pos = (-5, 1),
                                     antialias = True)
    right_resp_stim = visual.TextStim(win, font = "Arial", pos = (5, 1),
                                      antialias = True)

    # Responds position
    if (blocks[bn][0]['common_stim'] == 'O') and (blocks[bn][0]['common_resp'] == 'J'):
        left_resp_stim.text = f" {blocks[bn][0]['common_stim']}"
        right_resp_stim.text = f" {blocks[bn][0]['rare_stim']}"
    else:
        left_resp_stim.text = f" {blocks[bn][0]['rare_stim']}"
        right_resp_stim.text = f" {blocks[bn][0]['common_stim']}"

    # Draw all items
    block_break.draw()
    left_resp_stim.draw()
    right_resp_stim.draw()
    left_resp_key.draw()
    right_resp_key.draw()
    time_flip = win.flip()

    # Halt everything and wait for a response matching the keys
    # given in the Q object.
    key, time_key = event.waitKeys(keyList = config.COND_KEYS,
                                   timeStamped = True)[0]

    # Look at first reponse [0]. Quit everything if quit-key was pressed
    if key in config.KEYS_QUIT:
        log.flush()
        core.quit()
    return

def run_block(blocks, bn, config):
    """ Experimental block
    Taking in blocks and it current block number. Loop around list of dictionary,
    excute each trials in following column_order

    Block Excuting Order
    1. Start with Inter-block Interval
    2. Loop around whole a block of trials
        - ISI
        - stimulus on
        - Respond on
        - Log

    Input:
        blocks      : a list of list of dictionary with trial information
        bn          : block number
        config      : config.py with all specific configuration variables
        eeg         : Boolean value, if true setup parallel port.
    """
    # 1.Start fixation for Inter block interval.
    fix.draw()
    win.flip()
    core.wait(config.IBI) # Wait before experiment began.

    # Initate parallel port by reset back to 0
    pp_reset(eeg)

    for tr in range(len(blocks[bn])):
        # Start trial timer, also reset timmer for intra-trial RT
        if debug:
            print(f"Block {bn} Trial {tr} ...")
        tr_glob_time = glob_t.getTime()
        trial_time = trial_t.reset()

        ## Inter Stimulus Interval (ISI) ##
        # add jitter
        isi_dur = config.VISUAL_ISI+blocks[bn][tr]['isi_jit']

        for fr in range(isi_dur):
            fix.draw()
            win.flip()
            key = keypress(config)

            # Trial begin send a pluse
            if (fr == 0) and (eeg):
                pp.setData(config.TB_PIN)
                ISI=trial_t.getTime()

            elif fr == 0:
                ISI=trial_t.getTime()

            # debug
            if debug:
                print(f"ISI: {ISI}")

        # Reset pin back to 0 after stimulus presented.
        pp_reset(eeg)

        # ISI timing
        isi = trial_t.getTime()

        ## stimulus On ##
        for fr in range(config.VISUAL_DUR):
            stim_text.text = blocks[bn][tr]["stim"]
            stim_text.draw()
            win.flip()
            key = keypress(config)

            # stimulus presented send out a pluse
            if (fr == 0) and (eeg):
                pp.setData(config.STIM_PIN)

                # Log STIM_ON time w EEG timming
                stim_on = trial_t.getTime()

            # Log stimulus on time
            elif (fr == 0):
                stim_on = trial_t.getTime()

            # debug
            if debug:
                print("stim_on")
                print(trial_t.getTime())

        # Reset pin back to 0 after stimulus presented.
        pp_reset(eeg)

        ## Response On ##
        # Respond with Fixation
        #pygKey = event.getKeys()
        got_keys = 0

        # Response Duration
        # Start the trial rt timmer
        rt_t.reset()
        for fr in range(int(config.RESP_DUR)):
            # Stimulus present
            fix.draw()
            win.flip()

            # Key Press time
            key = keypress(config)
            rt = rt_t.getTime()
            press_glob_time = glob_t.getTime()

            # Log time
            if (key) and (got_keys == 0):
                # Boolean statement if got key and it is first key press given
                if eeg:
                    pp.setData(config.RESP_PIN)

                key_resp = key[0].capitalize()
                # Log: Trial log
                trial_log = dict(trial_num = tr+1,
                                  block_num = bn+1,
                                  press_glob_time = press_glob_time,
                                  rt = rt,
                                  response = key_resp,
                                  correct = key_resp == blocks[bn][tr]["correct_resp"],
                                  stim_on = stim_on,
                                  isi = isi,
                                  glob_init_time = tr_glob_time
                                  )
                # for debug
                got_keys += 1

    		    # Log and write out the trial
                tri_info = blocks[bn][tr]
                tri_info.update(trial_log)
                log.write(tri_info)

        # Miss response Log
        if got_keys == 0:
            # Log: Missing trial log
            trial_log = dict(trial_num = tr+1,
                              block_num = bn+1,
                              press_glob_time = press_glob_time,
                              rt = None,
                              response = None,
                              correct = False,
                              stim_on = stim_on,
                              isi = isi,
                              glob_init_time = tr_glob_time,
                              )
            # Log and write out the trial
            tri_info = blocks[bn][tr]
            tri_info.update(trial_log)
            log.write(tri_info)

def exp(blocks, config, glob_t, instruct):
    """Excute the Experiment
    Experiment flow:
        -   Instructions
            -   Initial instruction
            -   Familarized sample stimulus
            -   Final instructions before experiment begin
        -   Excute experimental

    Input:
        blocks   : A list of list of dictionary with conditions and trial information
        config   : Configuration file with all specific experimental definition
        glob_t : Global rt_t
        instruct : Instruction files with all the prompt instructions
    """
    exp_bg = glob_t.getTime()
    print(f"Experiment began machine time : {exp_bg} ...")

    ## Instructions ##
    prompt(instruct.init_inst)

    # Show examples
    for resp in config.STIMS:
        prompt(resp)

    # Final instructions before experiment start
    prompt(instruct.final_inst)

    # EEG PIN setup
    if eeg:
        if debug:
            print(f" BLOCK BEGAN : {glob_t.getTime()}")
        pp.setData(config.INIT_PIN)

    ## Initate Experimental ##
    for bn in range(len(blocks)):
        block_prompt(blocks, bn, config)
        # Beginning of each block
        if eeg:
            pp.setData(config.BB_PIN)
        run_block(blocks, bn, config)

    # EEG PIN setup
    if eeg:
        pp.setData(config.END_PIN)
        if debug:
            print(f" BLOCK ENDED : {glob_t.getTime()}")

    # Experiment End prompt
    prompt(instruct.finished_inst)

###########################
## (3).Excute Experiment ##
###########################
if __name__ == "__main__":
    if beh:
        # Run Experiment
        exp(blocks, config, glob_t, instruct)
        # debug
        if debug:
            exp_end = glob_t.getTime()
            print(f" Total Experimental Run time began : {mm_time} \n End : {exp_end}")
