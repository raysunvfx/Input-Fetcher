# Input-Fetcher

### What it does:
Input-Fetcher is a node organization system for the Foundry Nuke, which works on the idea of INPUTs and OUTPUTs.
<br>
Where INPUTs are child nodes, and OUTPUTs are parent nodes.


### How to use:
To call Input-Fetcher, use the hotkey "SHIFT + N" in Nuke:
![ Alt text](inputFetcher_00.gif)

Input-Fetcher has different functionality based on context.
<HR>
<summary>Labeller Context</summary>

Currently, we don't have any nodes selected, so it will by default create a "Dot" node and set the input text as its label:
![ Alt text](inputFetcher_01.gif)

If we call Input-Fetcher with a node selected however, any input we enter will be applied to the node as its label:
![ Alt text](inputFetcher_02.gif)

If multiple nodes are selected, all will receive the same label:
![ Alt text](inputFetcher_03.gif)
</HR>

To create an INPUT node: