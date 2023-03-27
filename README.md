# Input-Fetcher (WORK IN PROGRESS...)
<a href="https://vimeo.com/812094804/6a98ec1dad">WATCH INTRO VIDEO</a><br>
## What it does:

Input-Fetcher is a node organization system for the Foundry Nuke, which works on the idea of INPUTs and OUTPUTs.
<br><br>
It's a great solution for compositors who are looking to speed up their workflow and improve their script organization and mental clarity.

## Try the demo without installing:
Copy the contents of the demo.py and paste it into a new Nuke session's node graph.<br>
A brief introduction of Input Fetcher's features is laid out at the top of the script.<br>
Along with a mock script for testing things out!<br>
![ Alt text](media/inputFetcher_demo.gif)
<br>
## Installation:<br>
Downloading the inputFetcher_Zip.7z file and extract its contents.<br>

1. Go to your .nuke folder.<br>
2. Copy contents of init.py into your init.py.<br>
3. Copy contents of menu.py into your menu.py.<br>
4. Move the inputFetcher_v1.0 folder and its contents into your .nuke folder.<br>
5. OPTIONAL: In InputFetcherConfig.py, change the "_NODE_CLASS" value from 'Dot' to 'NoOp' if that's what you prefer!<br>
6. Launch Nuke and "Shift + N"!

## Quick Start Reference:</br>
Tag examples:</br>
'tag' - default tag command, will use tagged node's name as label.</br>
'tag new_label' - will use 'new_label' as tagged node's label.</br>
'tag lens dirt 35mm' - will use 'lens dirt 35mm' as tagged node's label.</br>
'untag' - untag node.</br>
</br>
Fetch examples:</br>
'OUT_PLATE_NATIVE' - create an output for category 'PLATE' named 'NATIVE'.</br>
'OUT_CAM_MAIN' - create an output for category 'CAM' named 'MAIN'.</br>
'OUT_MATTE_FG_CHAR_01' - creates an output for category 'MATTE' named 'FG_CHAR_01'.</br>
'OUT_SHIP_FLAG_03' - creates an output for category 'SHIP' named 'FLAG_03'.</br>
</br>
</br>
## How to use:

To call Input-Fetcher, use the hotkey "SHIFT + N" in Nuke:
![ Alt text](media/inputFetcher_00.gif)


Input-Fetcher has different functionality based on context.
There are three contexts:
1. Labeller
2. Input/Output
3. Commands

## Labeller Context



Currently, we don't have any nodes selected, so it will by default create a "Dot" node and set the input text as its label:<br>
![ Alt text](media/inputFetcher_01.gif)

If we call Input-Fetcher with a node selected however, any input we enter will be applied to the node as its label:<br>
![ Alt text](media/inputFetcher_02.gif)

If multiple nodes are selected, all will receive the same label:<br>
![ Alt text](media/inputFetcher_03.gif)


## Input / Output Context:<br>
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
![ Alt text](media/inputFetcher_04.gif)

Calling Input-Fetcher again, the newly created OUTPUT node will be visible in the UI, clicking it will create an INPUT node:
![ Alt text](media/inputFetcher_05.gif)

We can also create INPUT nodes by copy and pasting OUTPUT nodes:
![ Alt text](media/inputFetcher_06.gif)

Or by copy and pasting other INPUT nodes:
![ Alt text](media/inputFetcher_07.gif)

Or by converting one or more dot nodes:
![ Alt text](media/inputFetcher_08.gif)

Renaming an OUTPUT will update its children:
![ Alt text](media/inputFetcher_09.gif)

Use the hotkey "CTRL + C" to connect disconnected inputs:
![ Alt text](media/inputFetcher_10.gif)
