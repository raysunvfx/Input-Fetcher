# Input-Fetcher

## What it does:

Input-Fetcher is a node organization system for the Foundry Nuke, which works on the idea of INPUTs and OUTPUTs.
<br>


## How to use:

To call Input-Fetcher, use the hotkey "SHIFT + N" in Nuke:
![ Alt text](inputFetcher_00.gif)


Input-Fetcher has different functionality based on context.
There are three contexts:
1. Labeller
2. Input/Output
3. Commands
<HR></HR>
### Labeller Context



Currently, we don't have any nodes selected, so it will by default create a "Dot" node and set the input text as its label:
![ Alt text](inputFetcher_01.gif)

If we call Input-Fetcher with a node selected however, any input we enter will be applied to the node as its label:
![ Alt text](inputFetcher_02.gif)

If multiple nodes are selected, all will receive the same label:
![ Alt text](inputFetcher_03.gif)

<HR></HR>
### Input/Output Context:
Creating INPUTs and OUTPUTs is the main functionality of Input-Fetcher.<br>
To create an OUTPUT, we need to use this syntax:<br>
<p align="center">
<b>"OUT_PREFIX_LABEL"</b>
</p>

Here are the default prefixes that Input-Fetcher recognizes:

PLATE<br>
MATTE<br>
RENDER<br>
DEEP<br>
CAM<br>
GEO<br>

To create an OUTPUT for a plate, we can enter <b>"OUT_PLATE_NATIVE"</b>:
![ Alt text](inputFetcher_04.gif)

Calling Input-Fetcher again, the newly created OUTPUT node will be visible in the UI, clicking it will create an INPUT node:
![ Alt text](inputFetcher_05.gif)

We can also create INPUT nodes by copy and pasting OUTPUT nodes:
![ Alt text](inputFetcher_06.gif)

Or by copy and pasting other INPUT nodes:
![ Alt text](inputFetcher_07.gif)