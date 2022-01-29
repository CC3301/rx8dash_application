Collectors collect data from different endpoints in an asynchronous manner

The SensorAggregator asynchronously collects data from all the collectors and bundles it to be picked up by the GUI thread when ready

The GUI thread puts the collected data through the SensorDataProcessor which converts the values according to the 
configuration section "application:units". This could potentially also happen inside the SensorAggregator, in Order to
keep the GUI thread clean of any data processing.

Temperature Data is provided to the SensorAggregator in Kelvin
Distances and speeds are measured in the metric system by default

***Oil Pressure
- S1: 350 kPa {3.57 kgf/cm2, 50.8 psi} [3,000 rpm, oil temperature: 100 °C {212 °F}]
- S2: 500 kPa {5.10 kgf/cm2, 72.5 psi} [3,000 rpm, oil temperature: 100 °C {212 °F}]
- Series 2: Nominal regulator pressure 115 psi

***Oil Temperature
Operating Range = 190F – 230F Target Temp 200F
Terminal Temp = 250F (set alarm for 220F, due to 30-deg temp rise in the engine)
Warning light suggestion = High: 220F, Low: 160F

Oil Temp is measured on the Oil In side of the system (after oil coolers),
There is a 30 temperature rise within the engine, therefore a max ECU reading of 220 is approx. 250 exiting the engine


***Water Temperature
- Operating Range = 180F – 220F
- Terminal Temp = 240F
- *Map compensation starts at 212F
- Warning light suggestion = High: 220F, Low: 160F