SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+01:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données :  `bgpstreamdb`
--

-- --------------------------------------------------------

DROP TABLE IF EXISTS hijack;
DROP TABLE IF EXISTS outage;

--
-- Structure de la table `hijack`
--

CREATE TABLE `hijack` (
  `id` varchar(280) NOT NULL,
  `date` timestamp NULL DEFAULT NULL,
  `prefixe` varchar(280),
  `numASSource` varchar(280),
  `numASHijack` varchar(280)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Structure de la table `leak`
--

CREATE TABLE `outage` (
  `id` varchar(280) NOT NULL,
  `date` timestamp NULL DEFAULT NULL,
  `numAS` varchar(280),
  `nomAS` varchar(280),
  `paysAS` varchar(280),
  `nbPrefixe` varchar(280)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Index pour la table `hijack`
--
ALTER TABLE `hijack`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `outage`
--
ALTER TABLE `outage`
  ADD PRIMARY KEY (`id`);

  
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;


