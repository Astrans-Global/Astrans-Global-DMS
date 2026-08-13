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
exports.CreateItemService = void 0;
const lodash_1 = require("lodash");
const event_emitter_1 = require("@nestjs/event-emitter");
const common_1 = require("@nestjs/common");
const events_1 = require("../../common/events/events");
const ItemValidator_service_1 = require("./ItemValidator.service");
const Item_1 = require("./models/Item");
const UnitOfWork_service_1 = require("../Tenancy/TenancyDB/UnitOfWork.service");
const astransOpsExtras_1 = require("../AstransOps/astransOpsExtras");
let CreateItemService = class CreateItemService {
    constructor(eventEmitter, uow, validators, itemModel) {
        this.eventEmitter = eventEmitter;
        this.uow = uow;
        this.validators = validators;
        this.itemModel = itemModel;
    }
    async authorize(itemDTO) {
        await this.validators.validateItemNameUniquiness(itemDTO.name);
        if (itemDTO.categoryId) {
            await this.validators.validateItemCategoryExistance(itemDTO.categoryId);
        }
        if (itemDTO.sellAccountId) {
            await this.validators.validateItemSellAccountExistance(itemDTO.sellAccountId);
        }
        this.validators.validateIncomeAccountExistance(itemDTO.sellable, itemDTO.sellAccountId);
        if (itemDTO.costAccountId) {
            await this.validators.validateItemCostAccountExistance(itemDTO.costAccountId);
        }
        this.validators.validateCostAccountExistance(itemDTO.purchasable, itemDTO.costAccountId);
        if (itemDTO.inventoryAccountId) {
            await this.validators.validateItemInventoryAccountExistance(itemDTO.inventoryAccountId);
        }
        if (itemDTO.purchaseTaxRateId) {
            await this.validators.validatePurchaseTaxRateExistance(itemDTO.purchaseTaxRateId);
        }
        if (itemDTO.sellTaxRateId) {
            await this.validators.validateSellTaxRateExistance(itemDTO.sellTaxRateId);
        }
    }
    transformNewItemDTOToModel(itemDTO) {
        return {
            ...itemDTO,
            active: Boolean((0, lodash_1.defaultTo)(itemDTO.active, true)),
            quantityOnHand: itemDTO.type === 'inventory' ? 0 : null,
        };
    }
    async createItem(itemDTO, trx) {
        const { rest, extras } = astransOpsExtras_1.takeItemExtras(itemDTO);
        await this.authorize(rest);
        return this.uow.withTransaction(async (trx) => {
            const itemInsert = this.transformNewItemDTOToModel(rest);
            const item = await this.itemModel()
                .query(trx)
                .insertAndFetch({
                ...itemInsert,
            });
            await astransOpsExtras_1.upsertItemExtras(trx || this.itemModel().knex(), item.id, extras);
            await this.eventEmitter.emitAsync(events_1.events.item.onCreated, {
                item,
                itemId: item.id,
                trx,
            });
            return item.id;
        }, trx);
    }
};
exports.CreateItemService = CreateItemService;
exports.CreateItemService = CreateItemService = __decorate([
    (0, common_1.Injectable)({ scope: common_1.Scope.REQUEST }),
    __param(3, (0, common_1.Inject)(Item_1.Item.name)),
    __metadata("design:paramtypes", [event_emitter_1.EventEmitter2,
        UnitOfWork_service_1.UnitOfWork,
        ItemValidator_service_1.ItemsValidators, Function])
], CreateItemService);
//# sourceMappingURL=CreateItem.service.js.map