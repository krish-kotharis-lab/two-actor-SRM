README 
two-actor-SRM

#we use python3 
#on ciclad

module load python/3.6-anaconda50
conda create --name mypython36 python=3.6 -y
source activate mypython36

https://pypi.org/project/simple-pid/
pip install simple-pid

http://ivmech.github.io/ivPID/ 
https://github.com/ivmech/ivPID

test1.py  = simple test of the climate model and 1 global actor for SRM
test2.py  = we test 2 actors for SRM w/o knowledge of each other, two T setpoints
test3.py  = we test 2 actors for SRM with a NH / SH box model

When you are designing a PID controller for a given system, follow the steps 
shown below to obtain a desired response.
Obtain an open-loop response and determine what needs to be improved
Add a proportional control to improve the rise time
Add a derivative control to improve the overshoot
Add an integral control to eliminate the steady-state error
Adjust each of Kp, Ki, and Kd until you obtain a desired overall response. 
Keep in mind that you do not need to implement all three controllers (proportional, derivative, and integral) 
into a single system, if not necessary. For example, if a PI controller gives a good enough response, 
then you don't need to implement a derivative controller on the system. Keep the controller as simple as possible.

https://en.wikipedia.org/wiki/Integral_windup
http://brettbeauregard.com/blog/2011/04/improving-the-beginner%e2%80%99s-pid-reset-windup/
==> bound both the integral term and the total u term

MacMartin et al. 2014 
High gain Kp=1.2 %solar/°C   Ki=1.8 %solar/°C/yr
Low  gain Kp=0.6 %solar/°C   Ki=0.9 %solar/°C/yr 

1 %solar = 0.01 * 1370 / 4 * 0.7 = 2.4 Wm-2
High gain ==> Kp = 2.88 Wm-2/°C  et Ki = 4.32 Wm-2/°C/yr
Low gain  ==> Kp = 1.44 Wm-2/°C  et Ki = 2.16 Wm-2/°C/yr

------
Thoughts from the wikipedia entry for PID

No manual tuning possible for the climate system: very long timescales and not desirable ! 
but can tune on a model (even if the model is not perfect)

Non steady state because of warming in the pipeline- or could be seen as asymmetrical, easier to warm because forcing goes up

Feed forward control ?

Noise is not measurement noise but chaotic system, use low pass filter ?? 
