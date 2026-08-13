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
exports.CreateCustomer = void 0;
const common_1 = require("@nestjs/common");
const CreateEditCustomerDTO_service_1 = require("./CreateEditCustomerDTO.service");
const UnitOfWork_service_1 = require("../../Tenancy/TenancyDB/UnitOfWork.service");
const event_emitter_1 = require("@nestjs/event-emitter");
const Customer_1 = require("../models/Customer");
const events_1 = require("../../../common/events/events");
const astransOpsExtras_1 = require("../../AstransOps/astransOpsExtras");
let CreateCustomer = class CreateCustomer {
    constructor(uow, eventPublisher, customerDTO, customerModel) {
        this.uow = uow;
        this.eventPublisher = eventPublisher;
        this.customerDTO = customerDTO;
        this.customerModel = customerModel;
    }
    async createCustomer(customerDTO, trx) {
        const { rest, extras } = astransOpsExtras_1.takeContactExtras(customerDTO);
        const customerObj = await this.customerDTO.transformCreateDTO(rest);
        return this.uow.withTransaction(async (trx) => {
            await this.eventPublisher.emitAsync(events_1.events.customers.onCreating, {
                customerDTO: rest,
                trx,
            });
            const customer = await this.customerModel()
                .query(trx)
                .insertAndFetch({
                ...customerObj,
            });
            await astransOpsExtras_1.upsertContactExtras(trx || this.customerModel().knex(), customer.id, extras);
            await this.eventPublisher.emitAsync(events_1.events.customers.onCreated, {
                customer,
                customerId: customer.id,
                trx,
            });
            return customer;
        }, trx);
    }
};
exports.CreateCustomer = CreateCustomer;
exports.CreateCustomer = CreateCustomer = __decorate([
    (0, common_1.Injectable)(),
    __param(3, (0, common_1.Inject)(Customer_1.Customer.name)),
    __metadata("design:paramtypes", [UnitOfWork_service_1.UnitOfWork,
        event_emitter_1.EventEmitter2,
        CreateEditCustomerDTO_service_1.CreateEditCustomerDTO, Function])
], CreateCustomer);
//# sourceMappingURL=CreateCustomer.service.js.map