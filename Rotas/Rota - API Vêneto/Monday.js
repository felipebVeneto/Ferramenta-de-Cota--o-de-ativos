// Rota para obter informações de clientes
router.get('/clientes', authenticateUser, mondayController.getClientsInfo);

// Rota para obter informações de fundos exclusivos
router.get('/fundosExclusivos', mondayController.getExclusiveFundsInfo);

// Rota para obter informações de previdência
router.get('/previdencia', authenticateUser, mondayController.getPensionInfo);

// Rota para obter informações de investimento no exterior
router.get('/investimentoExterior', authenticateUser, mondayController.getOffshoreInvestmentInfo);

// Rota para obter informações de carteira administrada
router.get('/carteiraAdministrada', authenticateUser, mondayController.getManagedPortifolioInfo);

// Rota para obter informações de contas
router.get('/contas', authenticateUser, mondayController.getAccountsInfo);

// Rota para obter informações da relação entre clientes e produtos
router.get('/clienteTemProdutos', authenticateUser, mondayController.getClientHasProductsInfo);