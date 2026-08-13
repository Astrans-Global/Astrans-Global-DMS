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
exports.GetItemService = void 0;
const event_emitter_1 = require("@nestjs/event-emitter");
const common_1 = require("@nestjs/common");
const Item_1 = require("./models/Item");
const events_1 = require("../../common/events/events");
const TransformerInjectable_service_1 = require("../Transformer/TransformerInjectable.service");
const Item_transformer_1 = require("./Item.transformer");
const nestjs_cls_1 = require("nestjs-cls");
const astransOpsExtras_1 = require("../AstransOps/astransOpsExtras");
let GetItemService = class GetItemService {
    constructor(itemModel, eventEmitter2, transformerInjectable, clsService) {
        this.itemModel = itemModel;
        this.eventEmitter2 = eventEmitter2;
        this.transformerInjectable = transformerInjectable;
        this.clsService = clsService;
    }
    async getItem(itemId) {
        const item = await this.itemModel()
            .query()
            .findById(itemId)
            .withGraphFetched('sellAccount')
            .withGraphFetched('inventoryAccount')
            .withGraphFetched('category')
            .withGraphFetched('costAccount')
            .withGraphFetched('itemWarehouses.warehouse')
            .withGraphFetched('sellTaxRate')
            .withGraphFetched('purchaseTaxRate')
            .throwIfNotFound();
        const transformed = await this.transformerInjectable.transform(item, new Item_transformer_1.ItemTransformer());
        const extras = await astransOpsExtras_1.loadItemExtras(this.itemModel().knex(), itemId);
        const eventPayload = { itemId };
        await this.eventEmitter2.emitAsync(events_1.events.item.onViewed, eventPayload);
        return { ...transformed, ...extras };
    }
};
exports.GetItemService = GetItemService;
exports.GetItemService = GetItemService = __decorate([
    (0, common_1.Injectable)(),
    __param(0, (0, common_1.Inject)(Item_1.Item.name)),
    __metadata("design:paramtypes", [Function, event_emitter_1.EventEmitter2,
        TransformerInjectable_service_1.TransformerInjectable,
        nestjs_cls_1.ClsService])
], GetItemService);
//# sourceMappingURL=GetItem.service.js.map