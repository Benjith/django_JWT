from django.urls import include, path
from django.conf.urls import url
from .masters import accountType,chartofAccounts,party,gstRegistrationType,itemCategory,unitOfMeasures,taxCategory,warehouse,items
from .general import currencies,financialYears,country,state
from .transactions import invTransactionMaster,invTransactions,accTransactions
from .employees import employeeDesignations,employees
from . import imageUpload

urlpatterns = [   
# Haris
path('saveEmployeeDesignation/' ,employeeDesignations.saveEmployeeDesignation, name='saveEmployeeDesignation'),
path('getEmployeeDesignation/', employeeDesignations.getEmployeeDesignation, name='getEmployeeDesignation'),
path('deleteEmployeeDesignation/<int:deleteId>/', employeeDesignations.deleteEmployeeDesignation, name='deleteEmployeeDesignation'),
path('updateEmployeeDesignation/<int:updateId>/s', employeeDesignations.updateEmployeeDesignation, name='updateEmployeeDesignation'),

path('saveEmployee/' ,employees.saveEmployee, name='saveEmployee'),
path('getEmployee/', employees.getEmployee, name='getEmployee'),
path('deleteEmployee/<int:deletedId>/', employees.deleteEmployee, name='deleteEmployee'),
path('updateEmployee/<int:updatedId>/', employees.updateEmployee, name='updateEmployee'),
path('getEmployeeByID/<int:employeeID>/', employees.getEmployeeByID, name='getEmployeeByID'),

path('saveTaxCategory/' ,taxCategory.saveTaxCategory, name='saveTaxCategory'),
path('getTaxCategory/', taxCategory.getTaxCategory, name='getTaxCategory'),
path('deleteTaxCategory/', taxCategory.deleteTaxCategory, name='deleteTaxCategory'),
path('updateTaxCategory/', taxCategory.updateTaxCategory, name='updateTaxCategory'),

path('saveWarehouse/' ,warehouse.saveWarehouse, name='saveWarehouse'),
path('getWarehouse/', warehouse.getWarehouse, name='getWarehouse'),
path('deleteWarehouse/', warehouse.deleteWarehouse, name='deleteWarehouse'),
path('updateWarehouse/', warehouse.updateWarehouse, name='updateWarehouse'),

path('saveInvTransactions/',invTransactions.saveInvTransaction, name='SaveInventoryTransaction'),

path('saveAccTransactions/',accTransactions.saveAccTransaction, name='SaveAccentoryTransaction'),

path('getMaxVoucherNo/<str:voucharType>/',invTransactions.getMaxVoucherNo, name='getMaxVoucherNo'),

path('getTransactionDataById/<int:invTransactionMasterID>/',invTransactions.getTransactionDataById, name='getTransactionDataById'),

path('deleteTransactions/<int:id>/',invTransactions.delete, name='deleteInvTransactions'),
path('checkDuplicateRefNo/<str:referenceNo>/<int:partyAccID>/',invTransactions.checkDuplicateRefNo, name='checkDuplicateRefNo'),











# Benjith
#unit
path('addUnitOfMeasures/',unitOfMeasures.addUnitOfMeasures),
path('listAllUnit/',unitOfMeasures.listAllUnit),

#category & sub cat
path('addItemCategory/',itemCategory.addNewItemCategory),
path('listAllMainCategory/',itemCategory.listAllMainCategory),
path('listAllSubCategory/',itemCategory.listAllSubCategory),

#Item 
path('insertOrUpdateItem/',items.insertOrUpdateItem),
path('listAllItems/',items.listAllItems,),
path('deleteItemById/<int:itemID>/',items.deleteById,),
path('items/imageUpload/',imageUpload.ItemImgUpload),
path('deleteImageByName/<imageName>/',items.deleteImageByName),


#tax category


























#Muhsin

# save account type
path('saveAccType/' ,accountType.saveAccType, name='saveAccountType'), 
path('fetchAllAccType/',accountType.fetchAllAccType, name='fetch_all_account_type'),
path('deleteAccType/<int:accType_id>/',accountType.deleteAccType, name='deleteAccType'),

# Chart of account
path('saveChartOfAccount/',chartofAccounts.saveChartOfAcc, name='save_chart_of_account'),
path('fetchAllChartOfAccount/',chartofAccounts.fetchAllChartOfAccount,name='fetch_all_chart_of_account'),
path('fetchAllChartOfAccountForGridView/',chartofAccounts.fetchAllChartOfAccountForGrid,name='fetch_all_chart_of_account_for_gridView'),
path('delChartOfAcc/<int:accountID>/',chartofAccounts.deleteChartOfAccount, name='deleteChartOfAccount'),
path('editChartOfAcc/<int:id>/',chartofAccounts.editDetails, name='ChartOfAccountEditDetails'),
path('updateChartOfAcc/<int:id>/',chartofAccounts.updateChartOfAccount, name='updateChartOfAccount'),
path('accLedgerDetailsForEdit/<int:id>/' ,chartofAccounts.accLedgerDetailsForEdit, name='accLedgerDetailsForEdit'),

# Party
path('saveParty/' ,party.saveParty, name='saveParty'),
path('fetchAllPartyForGrid/' ,party.fetchAllPartyForGridView, name='fetchAllPartyForGrid'), 
path('partyLastCode/<str:PartyType>/' ,party.partyLastCode, name='partyLastCode'), 
path('deleteParty/<int:party_id>/' ,party.deleteParty, name='deleteParty'),
path('partyDetailsByID/<int:partyid>/' ,party.editParty, name='deleteParty'),
path('updateParty/<int:partyid>/' ,party.updateParty, name='updateParty'),
path('fetchAllParties/<str:partyType>/' ,party.fetchAllPartiesByType, name='fetchAllParties'), 
path('fetchAllPartiesByType/<str:partyType>/' ,party.fetchAllPartiesByType, name='fetchAllParties'),
path('partyDetailsByAccID/<int:accoutid>/' ,party.partyDetailsByAccID, name='partyDetailsByAccID'),

# GST Registration Type
path('fetchAllGSTRegType/' ,gstRegistrationType.fetchAllGSTRegType, name='fetchAllGSTRegType'),


# Country 
path('fetchAllCountry/' ,country.fetchAllCountry, name='fetchAllCountry'), 

# Country  
path('fetchAllState/<int:CountryID>/' ,state.fetchAllState, name='fetchAllState'), 

# Currencies
path('saveCurrency/' ,currencies.saveCurrencyDetails, name='saveCurrency'),
path('deleteCurrency/<int:currency_id>/' ,currencies.deleteCurrency, name='deleteCurrency'),

#Transaction setLatestVoucharNo
path('saveTransactions/',invTransactionMaster.saveInvTransactionMaster, name='SaveInventoryTransaction'),
path('setLatestVoucharNo/<str:voucharType>/',invTransactionMaster.setLatestVoucharNo, name='setLatestVoucharNo'),


#test
path('getBranch/' ,financialYears.saveCurrencyDetails, name='ffdfdfdfdfdfdf'), 

path('fetchAllItem/<str:itemType>/',items.fetchAllItem, name='fetchAllItem'),
path('fetchItemByID/<int:itemID>/',items.fetchItemByID, name='fetchItemByID'),
path('getItemByItemCode/<str:ItemCode>/',items.getItemByItemCode, name='getItemByItemCode'),
path('getItemByEAN_SKU/<str:EAN_SKU>/',items.getItemByEAN_SKU, name='getItemByEAN_SKU'),
path('getTaxCategoryById/<int:TaxCatID>/', taxCategory.getTaxCategoryById, name='getTaxCategoryById'),

path('fetchInvTransactionsForGrid/<str:voucherType>/',invTransactions.fetchInvTransactionsForGrid, name='fetchInvTransactionsForGrid'),
path('getTransactionMasterDataById/<int:invTransactionMasterID>/',invTransactions.getTransactionMasterDataById, name='getTransactionMastedDataById'),
path('getTransactionDetailsDataById/<int:invTransactionMasterID>/',invTransactions.getTransactionDetailsDataById, name='getTransactionDetailsDataById'),




]





