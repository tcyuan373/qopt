#!/usr/bin/python

import sys


from pylab import *

# DIM 50
XI = (
        0.465938, 
        0.416822, 
        0.415459, 
        0.497842, 
        0.311992, 
        )

DELTA = (
        0.986928,
        0.946898,
        0.934386,
        0.986275,
        0.898564,
        )

XI_worst = (
0.579114  ,
0.603145  ,
0.917436  ,
0.264703  ,
0.865176  ,
0.194553  ,
0.256631  ,
0.969614  ,
0.163682  ,
0.725037  ,
#0.736514  ,
0.887865  ,
0.817266  ,
0.60429   ,
0.69916   ,
)

DELTA_worst = (
   0.302611     ,
   0.293993     ,
   0.366648     ,
   0.0262873    ,
   0.303628     ,
   0.0358061    ,
   0.0273605    ,
   0.33598      ,
   0.014152     ,
   0.0734054    ,
   #0.998762     ,
   0.0528959    ,
   0.040472     ,
  0.0267464     ,
  0.020109      ,
)


# compared method 2
# l=\
# [(0.465938,0.986928),
# #(0.278267,0.904759),
# (0.364177,0.982871),
# (0.415459,0.934386),
# (0.416822,0.946898),
# (0.182157,0.937966),
# (0.255039,0.979016),]
# XI,DELTA= zip(*l)






#####################
# # DIM 30
#####################
#  XI = (0.364177,
#          0.416822,
#          0.560395,
#          0.465938,
#          0.497842)
#  
#  DELTA = (0.982871,
#          0.946898,
#          0.962158,
#          0.986928,
#          0.986275 )
#  
#  
#  XI_worst = (
#  0.499078   ,
#  0.361049   ,
#  #0.00393518 ,
#  0.969614   ,
#  0.200977   ,
#  0.194553   ,
#  0.163682   ,
#  #0.97304    ,
#  0.873573   ,
#  0.814767   ,
#  0.887865   ,
#  0.60429    ,
#  0.977294   ,
#  #0.736514   ,
#  0.729658   ,
#  )
#  
#  # compared method 2
#  l=[
#          (0.156456,0.939336),
#          (0.182157,0.937966),
#          (0.364177,0.982871),
#          (0.416822,0.946898),
#          (0.465938,0.986928),
#          (0.497842,0.986275),
#          (0.53769,0.967892),
#          (0.560395,0.962158),
#          (0.199516,0.88135),
#          (0.255039,0.979016),  
#          ]
#  XI,DELTA= zip(*l)
#  
#  
#  DELTA_worst = (
#    0.0947679     ,
#    0.0344567     ,
#      #0.938463    ,
#    0.33598       ,
#    0.0183306     ,
#    0.0358061     ,
#    0.014152      ,
#   #0.996816       ,
#    0.190194      ,
#    0.0681938     ,
#    0.0528959     ,
#   0.0267464      ,
#    0.0542578     ,
#    #0.998762      ,
#    0.0101053     ,
#  )




####################################
# DIM 10
####################################
#   XI = (
#           0.638822,
#           0.53769, 
#           0.650384,
#           0.62614, 
#           0.508857,
#           0.489323,
#           )
#   
#   DELTA = (
#           0.898101  ,
#           0.967892  ,
#           0.95879   ,
#           0.975676  ,
#           0.880632  ,
#           0.913706  ,
#           )
#   
#   
#   # compared method 2
#   l= [
#           (0.638822,0.898101),
#           #(0.782102,0.859613),
#           #(0.922773,0.853186),
#           (0.474405,0.943072),
#           (0.489323,0.913706),
#           (0.53769,0.967892),
#           (0.581875,0.921341),
#           (0.508857,0.880632),
#           (0.560395,0.962158),
#           (0.650384,0.95879),]
#   XI,DELTA= zip(*l)
#   
#   XI_worst = (
#   0.0191608  ,
#   0.105546   ,
#   0.0670178  ,
#   0.0934853  ,
#   0.163682   ,
#   0.0126948  ,
#   0.0727609  ,
#   0.719378   ,
#   0.046576   ,
#   0.0703358  ,
#   0.00393518 ,
#   0.00898533 ,
#   0.00749342 ,
#   )
#   
#   DELTA_worst = (
#      0.874844      ,
#     0.400585       ,
#      0.352891      ,
#      0.111135      ,
#     0.014152       ,
#      0.957948      ,
#      0.287763      ,
#     0.00203776     ,
#     0.236395       ,
#      0.0789305     ,
#       0.938463     ,
#       0.799368     ,
#       0.570414     ,
#   )




# DIM 2  -- bez zadnych zabiegow
# XI = (
#         0.734905,
#         0.924851,
#         0.882488,
#         0.745135,
#         #0.711523,
#         #0.810707,
#         #0.977657,
#         )
# 
# DELTA = (
#         0.698213 ,
#         0.544629 ,
#         0.643563 ,
#         0.721118 ,
#         #0.717335 ,
#         #0.478629 ,
#         #0.420812
#         )

# compared method 2
l= [
        (0.891907,0.703279,),
#        (0.89777,0.195825,),
#        (0.90078,0.229929,),
#        (0.928801,0.215631,),
#        (0.930072,0.27905,),
#        (0.930717,0.462274,),
#        (0.933386,0.369443,),
        (0.941205,0.680186,),
        (0.944633,0.349868,),
        (0.748923,0.638569,),
        (0.75426,0.745423,),
        (0.823639,0.739415,),
        (0.882488,0.643563,),
        ]
#l = [
#        (0.401577,0.812432),
#(0.474645,0.787938),
#(0.603145,0.293993),
#(0.609657,0.319252),
#(0.612411,0.792304),
#(0.703545,0.794154),
#(0.732811,0.773718),
#(0.792768,0.785005),
#(0.955577,0.789475),
#(0.418792,0.386698),
#(0.579114,0.302611),
#(0.591414,0.77766),
#(0.741737,0.75595),
#(0.887865,0.0528959),
#(0.969614,0.33598),
#(0.865176,0.303628),
#        ]
XI,DELTA= zip(*l)




#    # DIM2  --   ponizsze sa sposrod punktow, ktore byly probkowane dla wszystkich wymiarowosci
#    XI = (
#    0.741737 , 
#    0.955577 , 
#    0.792768 , 
#    0.936261 , 
#    #  0.910939 , 
#    #  0.93194  , 
#    #  0.732811 , 
#            )
#    
#    DELTA = (
#    
#       0.75595       , 
#       0.789475      , 
#       0.785005      , 
#       0.917006      , 
#    #   0.898484      ,       
#    #  0.76188        , 
#    #   0.773718      , 
#    )
#    
#    
XI_worst = (
0.00644673  ,
0.0346603   ,
0.00393518  ,
0.028626    ,
0.0025388   ,
0.00917114  ,
0.00280517  ,
0.00198027  ,
0.00187413  ,
)

DELTA_worst = (
0.905895    ,
0.00438882   ,
0.938463    ,
0.00668218    ,
0.679524     ,
0.0541838   ,
0.230395    ,
0.0992839   ,
0.0976963   ,
)







xlim(0,1)
ylim(0,1)
xlabel('$\\xi$')
ylabel('$\\delta$')

plot(XI,DELTA, 'go', markersize=10)
plot(XI_worst,DELTA_worst, 'dr', markersize=10)

savefig('/tmp/plot2d.pdf', bbox_inches='tight')

