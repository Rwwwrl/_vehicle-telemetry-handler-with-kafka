У нас есть два МСа: vehicle-geometry-intersection-ms и vehicle-loading-unloading-ms. У нас есть vehicle-mock-telemetry-generator, который пушит эвенты о составе, вот все эвенты по хронологическому порядку: [VehicleDidMovement, VehicleArrivedToLoadingArea, VehicleStartedLoading, VehicleFinishedLoading, VehicleDeparturedFromLoadingArea, …, VehicleDidMovement]

Требования:

1. Обработкой эвентов [VehicleDidMovement, VehicleArrivedToLoadingArea, VehicleDeparturedFromLoadingArea] занимается vehicle-geometry-intersection-ms.
2. Обработкой эвентов [VehicleStartedLoading, VehicleFinishedLoading] занимается vehicle-loading-unloading-ms
3. Мы должны обеспечить FIFO согласованность по vehicle_id - Если vehicle-geometry-intersection-ms получил эвент VehicleDeparturedFromLoadingArea для vehicle_id=10, то он может быть уверен, что VehicleArrivedToLoadingArea для vehicle_id=10 было обработано
