# README: Система Управления Ремонтной Компанией (Repair Company Management System)

- Классы: 50
- Поля: 193
- Уникальные поведения: 175
- Ассоциации: 67
- Исключения: 12

## Исключения (12)
Все в классе Exceptions (статические методы для throw):
- throwRepairCompanyException("Общая ошибка системы")
- throwInsufficientFundsException("Недостаточно средств")
- throwInvalidClientDataException("Недопустимые данные клиента")
- throwOrderNotFoundException("Заказ не найден")
- throwInvalidOrderDataException("Недопустимые данные заказа")
- throwInvalidPartDataException("Недопустимые данные детали")
- throwPartNotAvailableException("Деталь недоступна")
- throwServiceNotAvailableException("Услуга недоступна")
- throwTechnicianNotAvailableException("Техник недоступен")
- throwInvalidPaymentDataException("Недопустимые данные платежа")
- throwWarrantyExpiredException("Гарантия истекла")
- throwRepairQualityException("Проблема с качеством ремонта")

## Классы
Формат: Класс Поля Методы → Ассоциации (классы как поля/параметры)

Client 8 8 → Address, RepairOrder, Payment, BankAccount, Appointment, Invoice, Warranty, Feedback
- Поля: clientId, name, email, phone, address, balance, loyaltyPoints, repairHistory
- Методы: addFunds, deductFunds, transferToAnotherClient, addLoyaltyPoints, calculateDiscount, calculateLoyaltyTier, validateClientData, getRepairHistory

Address 6 5 → Client, Employee, Supplier, Warehouse
- Поля: street, city, state, zipCode, country, buildingNumber
- Методы: getFullAddress, validateAddressData, calculateDistance, formatForMailing, isValid

Employee 8 6 → Address, RepairOrder, Manager, Department
- Поля: employeeId, firstName, lastName, position, salary, hireDate, department, address, specialization, isAvailable, assignedOrders
- Методы: getFullName, assignOrder, completeOrder, updatePerformanceRating, calculateYearsOfService, calculateSalaryWithBonus

Technician 8 10 → Employee, RepairOrder, RepairService, Tool
- Поля: skillLevel, toolsCertification, completedRepairsCount, averageRepairTime, specializedEquipment, qualityRating, efficiencyScore, currentWorkload
- Методы: addEquipmentCertification, calculateEfficiencyScore, updateRepairStats, findCompatibleServices, updateQualityRating, calculateProductivity, requestTools, updateCertifications, validateSkills, canHandleComplexRepair

RepairService 9 6 → RepairOrder, Technician, InventoryItem
- Поля: serviceId, name, description, baseCost, estimatedHours, requiredParts, skillLevelRequired, warrantyPeriod, isAvailable
- Методы: calculateFinalCost, checkTechnicianQualification, getRequiredPartsList, validateServiceData, isComplexService, calculateComplexityScore

InventoryItem 9 7 → Supplier, RepairOrder, InventoryCategory
- Поля: partId, name, description, category, price, quantityInStock, minStockLevel, supplierInfo, compatibilityList
- Методы: checkAvailability, reserveItems, restockItems, needsRestocking, calculateTotalValue, validateInventoryData, updateSupplierInfo

RepairOrder 12 10 → Client, Technician, RepairService, InventoryItem, Payment, Warranty
- Поля: orderId, client, deviceDescription, problemDescription, serviceRequired, technicianAssigned, priorityLevel, creationDate, status, actualHours, usedParts, totalCost
- Методы: addUsedPart, calculateTotalCost, markInProgress, markCompleted, checkWarrantyStatus, calculateRepairComplexity, validateOrderData, getStatusHistory, estimateCompletionTime, applyDiscount

Payment 8 7 → Client, RepairOrder, BankAccount, Invoice
- Поля: paymentId, client, repairOrder, amount, paymentMethod, paymentDate, isProcessed, transactionId
- Методы: processPayment, generateReceipt, processInstallmentPlan, validatePaymentMethod, refundPayment, calculateTax, generatePaymentReport

BankAccount 5 7 → Client, Employee, Transaction, Invoice
- Поля: accountNumber, accountHolder, bankName, balance, currency, transactionHistory
- Методы: transferToAnotherAccount, calculateInterest, validateAccountNumber, getTransactionStatistics, applyFee, generateStatement, closeAccount

Invoice 10 12 → RepairOrder, Client, Payment, BankAccount
- Поля: invoiceId, repairOrder, client, issueDate, dueDate, lineItems, totalAmount, paidAmount, status, taxAmount
- Методы: addLineItem, removeLineItem, addPayment, isOverdue, calculateRemainingBalance, applyEarlyPaymentDiscount, generateInvoicePdf, sendPaymentReminder, calculateLateFee, validateInvoiceData, getPaymentHistory, calculateTax

Warranty 6 5 → RepairOrder, WarrantyClaim, Client
- Поля: warrantyId, repairOrder, durationDays, startDate, termsConditions, claimsCount
- Методы: isValid, registerClaim, calculateExpiryDate, validateWarrantyClaim, generateWarrantyCertificate

Appointment 7 5 → Client, Technician, RepairService
- Поля: appointmentId, client, technician, scheduledDate, durationHours, serviceType, status
- Методы: reschedule, cancelAppointment, confirmAppointment, sendReminder, checkAvailability

Supplier 8 4 → Address, InventoryItem, PurchaseOrder
- Поля: supplierId, name, contactPerson, phone, email, address, rating, deliveryTimeDays
- Методы: calculateReliabilityScore, updateRating, getContactInfo, validateSupplierData

PurchaseOrder 8 6 → Supplier, InventoryItem, Warehouse
- Поля: orderId, supplier, items, orderDate, expectedDelivery, totalAmount, status, receivedItems
- Методы: processDelivery, updateStatus, calculateTotal, validateOrder, trackDelivery, generatePoReport

Manager 10 6 → Employee, RepairOrder, Department, Budget
- Поля: teamSize, budgetResponsibility, managedEmployees, approvedOrders
- Методы: approveRepairOrder, assignEmployeeToDepartment, calculateTeamProductivity, manageBudget, generatePerformanceReport, approveExpense

Receptionist 10 6 → Client, Appointment, Payment
- Поля: shiftSchedule, languages, processedAppointments
- Методы: handlePhoneInquiry, generateDailySchedule, registerClient, scheduleAppointment, processPaymentAtDesk, generateReceptionReport

ServicePackage 8 6 → RepairService, Client, Invoice
- Поля: packageId, name, description, includedServices, discountRate, validityPeriod, activeClients, terms
- Методы: calculatePackagePrice, addClientToPackage, removeClientFromPackage, isValid, getServicesList, applyPackageDiscount

QualityInspection 7 5 → RepairOrder, Technician, QualityControlManager
- Поля: inspectionId, repairOrder, inspector, inspectionDate, criteria, passed, notes
- Методы: performInspection, generateInspectionReport, retestRepair, approveRepair, failRepair

ServiceCategory 6 5 → RepairService, Department
- Поля: categoryId, name, description, parentCategory, services, averageCompletionTime
- Методы: getAllServicesRecursive, calculateCategoryRevenue, addService, removeService, findServiceByName

InventoryCategory 6 5 → InventoryItem, Warehouse
- Поля: categoryId, name, description, parentCategory, items, maxCapacity
- Методы: getTotalCategoryValue, getLowStockItems, addItem, removeItem, checkCapacity

WarrantyClaim 9 6 → Warranty, RepairOrder, Payment
- Поля: claimId, warranty, repairOrder, claimDate, description, supportingDocs, status, approvedAmount, resolutionDate
- Методы: evaluateClaim, approveClaim, rejectClaim, processRefund, uploadSupportingDocs, trackClaimStatus

FinancialReport 7 6 → Transaction, Invoice, BankAccount
- Поля: reportId, periodStart, periodEnd, generatedBy, transactions, invoices, revenue, expenses
- Методы: calculateFinancialMetrics, generateReportSummary, exportToPdf, addTransaction, removeTransaction, compareWithPreviousPeriod

Transaction 9 6 → BankAccount, Invoice, Payment
- Поля: transactionId, fromAccount, toAccount, amount, transactionType, description, timestamp, status, referenceNumber
- Методы: executeTransfer, generateTransactionReceipt, validateTransaction, reverseTransaction, addNote, getTransactionDetails

Salary 9 7 → Employee, BankAccount, TaxRecord
- Поля: salaryId, employee, baseSalary, paymentDate, isPaid, overtimePay, bonuses, deductions, taxAmount
- Методы: calculateTotalSalary, processPayment, addOvertime, addBonus, applyDeduction, calculateTax, generatePayslip

RepairServiceManager 5 10 → RepairOrder, Technician, RepairService
- Поля: activeOrders, completedOrders, availableTechnicians, repairServices, serviceQueue
- Методы: createRepairOrder, assignTechnicianToOrder, completeRepairOrder, calculateTechnicianWorkload, findAvailableTechnician, prioritizeOrders, trackOrderStatus, estimateCompletionTime, generateServiceReport, optimizeSchedule

InventoryManager 5 8 → InventoryItem, Supplier, PurchaseOrder
- Поля: inventoryItems, suppliers, restockRequests, inventoryCategories, lowStockAlerts
- Методы: addInventoryItem, findItemById, checkPartAvailability, processRestockRequests, calculateTotalInventoryValue, generateInventoryReport, optimizeStockLevels, trackItemUsage

QualityControlManager 5 7 → QualityInspection, Technician, RepairOrder
- Поля: qualityStandards, inspections, qualityMetrics, improvementPlans, auditLogs
- Методы: performQualityInspection, generateQualityReport, analyzeDefectPatterns, implementImprovements, trainTechnicians, monitorCompliance, calculateQualityScore

UserAccount 10 8 → Employee, AccessControl, SecurityLog
- Поля: userId, username, passwordHash, email, role, createdDate, lastLogin, isActive, failedLoginAttempts, securityQuestions
- Методы: verifyPassword, resetPassword, checkAccountLockStatus, validatePasswordStrength, generatePasswordRecoveryToken, updateProfile, logActivity, enableTwoFactorAuth

AccessControl 7 6 → UserAccount, SecurityLog, Resource
- Поля: controlId, userRole, resourceType, permissions, conditions, assignedUsers, accessLogs
- Методы: checkPermission, assignToUser, revokeAccess, updatePermissions, auditAccess, validateAccessRequest

SecurityLog 8 6 → UserAccount, AccessControl, SystemEvent
- Поля: logId, userAccount, action, timestamp, ipAddress, status, details, severityLevel
- Методы: logSecurityEvent, analyzeSuspiciousActivity, generateSecurityReport, alertAdministrator, archiveLogs, searchLogs

Department 6 6 → Employee, Budget, Asset
- Поля: departmentId, name, manager, employees, budget, location, assets
- Методы: addEmployee, removeEmployee, calculateDepartmentCost, allocateBudget, trackPerformance, generateDepartmentReport

Tool 5 5 → Technician, InventoryItem
- Поля: toolId, name, type, condition, lastMaintenanceDate, assignedTechnician
- Методы: assignToTechnician, performMaintenance, checkCondition, calculateDepreciation, scheduleMaintenance

Vehicle 6 5 → Employee, GPSPosition, Insurance
- Поля: vehicleId, model, year, licensePlate, currentDriver, gpsDevice, insurancePolicy
- Методы: assignDriver, trackLocation, calculateMaintenanceSchedule, updateInsurance, generateUsageReport

Training 6 4 → Technician, Department
- Поля: trainingId, title, trainer, participants, duration, completionDate, status
- Методы: registerParticipant, markCompleted, generateCertificate, evaluateTraining

Audit 7 5 → Department, Manager, System
- Поля: auditId, auditor, department, auditDate, findings, recommendations, status
- Методы: conductAudit, generateReport, implementRecommendations, trackProgress, verifyCompliance

Budget 5 5 → Department, Manager
- Поля: budgetId, department, fiscalYear, allocatedAmount, spentAmount, categories
- Методы: allocateFunds, trackSpending, calculateRemaining, requestAdditional, generateBudgetReport

TaxRecord 6 4 → Employee, Company
- Поля: recordId, employee, taxYear, taxableIncome, taxAmount, paymentStatus
- Методы: calculateTax, processPayment, generateTaxForm, verifyCompliance

LoyaltyProgram 5 4 → Client, Marketing
- Поля: programId, name, tierRules, benefits, enrolledClients, startDate
- Методы: enrollClient, calculateTier, awardPoints, redeemBenefits, analyzeProgramEffectiveness

Feedback 6 4 → Client, RepairOrder
- Поля: feedbackId, client, repairOrder, rating, comments, date, status
- Методы: submitFeedback, calculateAverageRating, generateReport, respondToFeedback

Notification 6 4 → UserAccount, System
- Поля: notificationId, recipient, type, message, priority, sentDate, readStatus
- Методы: sendNotification, markAsRead, setPriority, archiveNotification

Schedule 5 5 → Employee, Appointment
- Поля: scheduleId, employee, date, appointments, availability, conflicts
- Методы: addAppointment, removeAppointment, checkAvailability, resolveConflicts, generateScheduleReport

Report 5 4 → Manager, Department
- Поля: reportId, type, generatedBy, data, generationDate, format
- Методы: generateReport, exportToFormat, scheduleGeneration, analyzeData

Contract 6 5 → Client, Manager, Legal
- Поля: contractId, client, manager, startDate, endDate, terms, status
- Методы: createContract, reviewTerms, signContract, terminateContract, renewContract

Insurance 5 4 → Vehicle, Asset, Company
- Поля: policyId, insuredItem, provider, coverageAmount, premium, expirationDate
- Методы: calculatePremium, fileClaim, renewPolicy, checkCoverage

Expense 5 5 → Department, Employee
- Поля: expenseId, department, employee, amount, category, date, status
- Методы: submitExpense, approveExpense, rejectExpense, trackExpenses, generateExpenseReport

Asset 6 4 → Department, Company
- Поля: assetId, name, type, department, purchaseDate, value, depreciationRate
- Методы: calculateDepreciation, performMaintenance, transferDepartment, disposeAsset

Project 6 5 → Manager, Department, Budget
- Поля: projectId, name, manager, team, budget, startDate, endDate, status
- Методы: planProject, assignResources, trackProgress, calculateBudgetUsage, completeProject

Metric 5 4 → Department, System
- Поля: metricId, name, department, value, target, period
- Методы: calculateValue, compareToTarget, analyzeTrend, generateMetricReport

Alert 5 4 → System, UserAccount
- Поля: alertId, type, severity, recipient, message, timestamp, status
- Методы: triggerAlert, acknowledgeAlert, escalateAlert, resolveAlert

Configuration 5 4 → System, Company
- Поля: configId, system, settings, lastUpdated, version, environment
- Методы: loadConfiguration, saveConfiguration, validateSettings, backupConfig

IClient 0 13
- Методы: getClientId, getName, getAddress, getPhoneNumber, getEmail, setEmail, setPhoneNumber, updateContactInfo, getOrders, placeOrder, getDiscountRate, getLoyaltyPoints, getLastOrderDate

IOrder 0 12
- Методы: getOrderId, getPassengers, getPaymentType, getCargoWeight, getVehicle, getStatus, setStatus, calculateCost, getTotalCost, createOrder, getCustomer, assignVehicleAndEmployee

IService 0 10
- Методы: getServiceId, getName, getDescription, getBaseCost, getEstimatedHours, checkTechnicianQualification, calculateFinalCost, isAvailable, getRequiredParts, validateServiceData
