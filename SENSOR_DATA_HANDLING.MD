Collectors collect data from different endpoints in an asynchronous manner

The SensorAggregator asynchronously collects data from all the collectors and bundles it to be picked up by the GUI thread when ready

The GUI thread puts the collected data through the SensorDataProcessor which converts the values according to the 
configuration section "application:units". This could potentially also happen inside the SensorAggregator, in Order to
keep the GUI thread clean of any data processing.

Temperature Data is provided to the SensorAggregator in Kelvin
Distances and speeds are measured in the metric system by default

