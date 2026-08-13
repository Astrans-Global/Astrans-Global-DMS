"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var __param = (this && this.__param) || function (paramIndex, decorator) {
    return function (target, key) { decorator(target, key, paramIndex); }
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.GetCustomerService = void 0;
const common_1 = require("@nestjs/common");
const CustomerTransformer_1 = require("./CustomerTransformer");
const TransformerInjectable_service_1 = require("../../Transformer/TransformerInjectable.service");
const Customer_1 = require("../models/Customer");
const astransOpsExtras_1 = require("../../AstransOps/astransOpsExtras");
let GetCustomerService = class GetCustomerService {
    constructor(transformer, customerModel) {
        this.transformer = transformer;
        this.customerModel = customerModel;
    }
    async getCustomer(customerId) {
        const customer = await this.customerModel()
            .query()
            .findById(customerId)
            .throwIfNotFound();
        const transformed = await this.transformer.transform(customer, new CustomerTransformer_1.CustomerTransfromer());
        const extras = await astransOpsExtras_1.loadContactExtras(this.customerModel().knex(), customerId);
        return { ...transformed, ...extras };
    }
};
exports.GetCustomerService = GetCustomerService;
exports.GetCustomerService = GetCustomerService = __decorate([
    (0, common_1.Injectable)(),
    __param(1, (0, common_1.Inject)(Customer_1.Customer.name)),
    __metadata("design:paramtypes", [TransformerInjectable_service_1.TransformerInjectable, Function])
], GetCustomerService);
//# sourceMappingURL=GetCustomer.service.js.map