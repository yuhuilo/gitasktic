""" List Generation for ODDBALL experiment.
created by Paul Z. Cheng

"""

import random
import config

debug = True

# List Generation
# Each stim as rare
# Each response mapped to each stimulus
def list_gene(config):
    """generate oddball experimental list
    Counter balance mapping :

    Stimulus conditon X Stimulus Response Mapping
     (Common vs Rare) X (Left vs Right)

    input: config.py file with following definition.
                STIMS   : stimulus types
                RESPS   : response keys
                CONDS   : experimental condition
                NUM_REPT: each rep is 4 condition.
    Output:
          blocks : a list of list of dictionary with all
		   trial information.
    """
    blocks = []
    # Each counterbalanced block as four blocks
    # additional blocks adjust the number of repition.
    for b in range(config.NUM_REPT):
        # Create counter balance blocks
        for reverse_stim in [True, False]:
            # pick the proper stim set
            stims = config.STIMS
            # reverse if required
            if reverse_stim:
                stims = stims[::-1]

            # map to common and rare
            stim = {'common':stims[0],
                    'rare':stims[1]}

            # loop over response mappings
            for reverse_resp in [True, False]:
                # pick the responses
                resps = config.RESPS[:]
                if reverse_resp:
                    resps = resps[::-1]
                # make the mapping
                resp = {'common':resps[0],
                        'rare':resps[1]}

                # shuffle the conds
                random.shuffle(config.CONDS)
                
                # Generate jitter range
                jitter_range = [i+1 for i in range(config.JITTER)]
                random.shuffle(jitter_range)
                random.shuffle(jitter_range)
                
                # make the block
                block = [{'cond':cond,
                          'common_stim':stim['common'],
                          'rare_stim':stim['rare'],
                          'common_resp':resp['common'],
                          'rare_resp':resp['rare'],
                          'stim':stim[cond],
                          'correct_resp':resp[cond],
                          'isi_jit':jitter_range[0]}
                         for cond in config.CONDS]

                # append to blocks
                blocks.append(block)

    # shuffle the blocks
    random.shuffle(blocks)

    #return all the block
    return blocks

# Debug
if debug:
    blocks=list_gene(config)
    print(len(blocks[0]))
