# WheelsWithDice

## Requirements

Wheel: pygame, matplot.lib
Dice: matplot.lib

## Usage:

The dice is very customisable being compatible with n sides and also being able to handle weighted sides (see wheels/sample/loadedd6.txt)

The wheel inherits the dice which it will use to spin, similar to what appears on wheelofnames

## Why this is different

The main reason why this dice and by extension the wheel is different is because of the way it handles the rare cases, often with random number generators, there isn't any guarantee that you will ever get a certain outcome, however with this, there is no longer that possibility (well it is extremely unlikely)