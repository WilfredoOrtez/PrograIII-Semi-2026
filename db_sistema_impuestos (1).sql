-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 21-10-2026 a las 21:30:35
-- Versión del servidor: 10.4.18-MariaDB
-- Versión de PHP: 8.0.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `db_sistema_impuestos`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

CREATE TABLE `clientes` (
  `idCliente` int(10) NOT NULL,
  `codigo` char(10) NOT NULL,
  `nombre` char(100) NOT NULL,
  `direccion` char(150) NOT NULL,
  `telefono` char(10) NOT NULL,
  `email` char(150) NOT NULL,
  `tipo` char(10) NOT NULL DEFAULT 'particular'
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `clientes`
--

INSERT INTO `clientes` (`idCliente`, `codigo`, `nombre`, `direccion`, `telefono`, `email`, `tipo`) VALUES
(2, '002', 'josue', 'jan miguel', '3233-2232', 'holq@gmail.com', 'empresa'),
(3, '003', 'Empresa Prueba Modificada', 'Usulutan', '7000-0000', 'prueba@gmail.com', 'empresa');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `periodos`
--

CREATE TABLE `periodos` (
  `id` int(11) NOT NULL,
  `cliente_id` int(11) NOT NULL,
  `producto_id` int(11) NOT NULL,
  `desde` date NOT NULL,
  `hasta` date NOT NULL,
  `balance` decimal(15,2) NOT NULL,
  `tarifa_id` int(11) NOT NULL,
  `precio_calculado` decimal(15,2) NOT NULL,
  `formula_version` varchar(50) NOT NULL,
  `fecha_calculo` datetime NOT NULL DEFAULT current_timestamp(),
  `facturado` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `periodos`
--

INSERT INTO `periodos` (`id`, `cliente_id`, `producto_id`, `desde`, `hasta`, `balance`, `tarifa_id`, `precio_calculado`, `formula_version`, `fecha_calculo`, `facturado`) VALUES
(1, 2, 1, '2026-01-01', '2026-09-30', '545.00', 2, '4.50', 'bloques_v1', '2026-09-30 17:03:48', 0),
(2, 3, 1, '2026-02-03', '2026-09-22', '545.00', 2, '4.50', 'bloques_v1', '2026-09-30 17:29:22', 0),
(3, 3, 1, '2027-01-01', '2027-12-29', '1500.00', 3, '6.00', 'bloques_v1', '2026-09-30 17:31:25', 0),
(4, 3, 2, '2029-01-01', '2029-12-29', '545.00', 17, '4.50', 'bloques_v1', '2026-09-30 17:32:35', 0),
(5, 3, 2, '2030-01-01', '2030-11-29', '1500.00', 18, '6.00', 'bloques_v1', '2026-09-30 17:35:00', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `id` int(11) NOT NULL,
  `codigo` varchar(10) NOT NULL,
  `nombre` varchar(150) NOT NULL,
  `tipo` enum('comercio','industria') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`id`, `codigo`, `nombre`, `tipo`) VALUES
(1, '11801', 'Impuesto a las Actividades Economicas Comercio', 'comercio'),
(2, '11802', 'Impuesto a las Actividades Economicas Industria', 'industria');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tarifas`
--

CREATE TABLE `tarifas` (
  `id` int(11) NOT NULL,
  `producto_id` int(11) NOT NULL,
  `desde` decimal(15,2) NOT NULL,
  `hasta` decimal(15,2) NOT NULL,
  `precio_base` decimal(15,6) NOT NULL,
  `adicional` decimal(15,6) NOT NULL DEFAULT 0.000000,
  `porcentaje` decimal(8,4) NOT NULL DEFAULT 0.0000,
  `vigencia_desde` date NOT NULL,
  `vigencia_hasta` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `tarifas`
--

INSERT INTO `tarifas` (`id`, `producto_id`, `desde`, `hasta`, `precio_base`, `adicional`, `porcentaje`, `vigencia_desde`, `vigencia_hasta`) VALUES
(1, 1, '0.01', '500.00', '1.500000', '0.000000', '0.0000', '2020-01-01', NULL),
(2, 1, '500.01', '1000.00', '1.500000', '3.000000', '0.0000', '2020-01-01', NULL),
(3, 1, '1000.01', '2000.00', '3.000000', '3.000000', '0.0000', '2020-01-01', NULL),
(4, 1, '2000.01', '3000.00', '6.000000', '3.000000', '0.0000', '2020-01-01', NULL),
(5, 1, '3000.01', '6000.00', '9.000000', '2.000000', '0.0000', '2020-01-01', NULL),
(6, 1, '8000.01', '18000.00', '15.000000', '2.000000', '0.0000', '2020-01-01', NULL),
(7, 1, '18000.01', '30000.00', '39.000000', '2.000000', '0.0000', '2020-01-01', NULL),
(8, 1, '30000.01', '60000.00', '63.000000', '1.000000', '0.0000', '2020-01-01', NULL),
(9, 1, '60000.01', '100000.00', '93.000000', '0.800000', '0.0000', '2020-01-01', NULL),
(10, 1, '100000.01', '200000.00', '125.000000', '0.700000', '0.0000', '2020-01-01', NULL),
(11, 1, '200000.01', '300000.00', '195.000000', '0.600000', '0.0000', '2020-01-01', NULL),
(12, 1, '300000.01', '400000.00', '255.000000', '0.450000', '0.0000', '2020-01-01', NULL),
(13, 1, '400000.01', '500000.00', '300.000000', '0.400000', '0.0000', '2020-01-01', NULL),
(14, 1, '500000.01', '1000000.00', '340.000000', '0.300000', '0.0000', '2020-01-01', NULL),
(15, 1, '1000000.01', '99999999.99', '490.000000', '0.180000', '0.0000', '2020-01-01', NULL),
(16, 2, '0.01', '500.00', '1.500000', '0.000000', '0.0000', '2020-01-01', NULL),
(17, 2, '500.01', '1000.00', '1.500000', '3.000000', '0.0000', '2020-01-01', NULL),
(18, 2, '1000.01', '2000.00', '3.000000', '3.000000', '0.0000', '2020-01-01', NULL),
(19, 2, '2000.01', '3000.00', '6.000000', '3.000000', '0.0000', '2020-01-01', NULL),
(20, 2, '3000.01', '6000.00', '9.000000', '2.000000', '0.0000', '2020-01-01', NULL),
(21, 2, '8000.01', '18000.00', '15.000000', '2.000000', '0.0000', '2020-01-01', NULL),
(22, 2, '18000.01', '30000.00', '39.000000', '2.000000', '0.0000', '2020-01-01', NULL),
(23, 2, '30000.01', '60000.00', '63.000000', '1.000000', '0.0000', '2020-01-01', NULL),
(24, 2, '60000.01', '100000.00', '93.000000', '0.800000', '0.0000', '2020-01-01', NULL),
(25, 2, '100000.01', '200000.00', '125.000000', '0.700000', '0.0000', '2020-01-01', NULL),
(26, 2, '200000.01', '300000.00', '195.000000', '0.600000', '0.0000', '2020-01-01', NULL),
(27, 2, '300000.01', '400000.00', '255.000000', '0.450000', '0.0000', '2020-01-01', NULL),
(28, 2, '400000.01', '500000.00', '300.000000', '0.400000', '0.0000', '2020-01-01', NULL),
(29, 2, '500000.01', '1000000.00', '340.000000', '0.300000', '0.0000', '2020-01-01', NULL),
(30, 2, '1000000.01', '99999999.99', '490.000000', '0.180000', '0.0000', '2020-01-01', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios_usss019225`
--

CREATE TABLE `usuarios_usss019225` (
  `idUsuario` int(10) NOT NULL,
  `usuario` char(35) NOT NULL,
  `clave` char(35) NOT NULL,
  `nombre` char(85) NOT NULL,
  `direccion` char(100) NOT NULL,
  `telefono` char(9) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `usuarios_usss019225`
--

INSERT INTO `usuarios_usss019225` (`idUsuario`, `usuario`, `clave`, `nombre`, `direccion`, `telefono`) VALUES
(1, 'admin', '123', 'Wilfredo Ortez', 'Usulutan', '70073064');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`idCliente`);

--
-- Indices de la tabla `periodos`
--
ALTER TABLE `periodos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_cliente` (`cliente_id`),
  ADD KEY `idx_producto` (`producto_id`),
  ADD KEY `idx_tarifa` (`tarifa_id`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `codigo` (`codigo`);

--
-- Indices de la tabla `tarifas`
--
ALTER TABLE `tarifas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `producto_id` (`producto_id`);

--
-- Indices de la tabla `usuarios_usss019225`
--
ALTER TABLE `usuarios_usss019225`
  ADD PRIMARY KEY (`idUsuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `clientes`
--
ALTER TABLE `clientes`
  MODIFY `idCliente` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `periodos`
--
ALTER TABLE `periodos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `tarifas`
--
ALTER TABLE `tarifas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT de la tabla `usuarios_usss019225`
--
ALTER TABLE `usuarios_usss019225`
  MODIFY `idUsuario` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `periodos`
--
ALTER TABLE `periodos`
  ADD CONSTRAINT `fk_periodo_producto` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`),
  ADD CONSTRAINT `fk_periodo_tarifa` FOREIGN KEY (`tarifa_id`) REFERENCES `tarifas` (`id`);

--
-- Filtros para la tabla `tarifas`
--
ALTER TABLE `tarifas`
  ADD CONSTRAINT `tarifas_ibfk_1` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
