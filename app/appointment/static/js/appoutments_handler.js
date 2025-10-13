class ShopifySite extends JsForm {
    constructor(options) {
        super(options)
        this.shopDetails = {};
        this.object = {
            objbet:{},
            data:{}
        }
        this.get(`//${this.options.appUrl}appointment/request/1/1/${this.options.userId?$this.options.userId.split.pop():'none'}`).then(result=>{
            this.data.staffUser=result.staffUser;
            this.data.slots = result.slotsAvailable;
            this.data.userDetails = result.userDetails
            this.render()
        })
    }
    closer() {
        return ()=>this.render()
    }
    formName() {
        return "shopForm";
    }

    formContents() {
        return `
            <div class="formRow">
                <div class="formField">
                    <label>First Name
                    <label>Shop Name</label>
                    <div><input type="text" autocomplete="off" name="shopName" value="${this.shopDetails.shopName||""}" required></div>
                </div>
                <div class="formField">
                    <label>Shop Domain</label>
                    <div class="labelledInput"><input autocomplete="off" type="text" name="shopDomain" value="${this.shopDetails.shopDomain||""}" required>.myshopify.com</div>
                </div>
            </div>
            <div class="formRow">
                <div class="formField">
                    <label>App Key</label>
                    <div><input type="text" autocomplete="off" name="appKey" value="${this.shopDetails.appKey||""}" required></div>
                </div>
                <div class="formField">
                    <label>Access Token</label>
                    <div class="labelledInput">
                        <input type="password" autocomplete="off" name="authToken" value="${this.shopDetails.authToken||""}" required>
                        <img src="/static/img/peek.png" data-for="authToken" class="peeker">
                    </div>
                </div>
            </div>
        `;
    }
    buttons() {
        return [
            [
                {label:`Update ${this.shopDetails.shopName}`,action:"update",class:'requires-id',type:"submit"},
                {label:'Create Shop',action:"create",class:'create-only',type:"submit"},
                {label:`Delete ${this.shopDetails.shopName}`,action:"delete",class:'requires-id'},
            ],
            [
                {label:'Deploy Theme Files',action:"theme-files",class:'requires-id'},
                
            ]
        ]
    }
    setupEvents() {
        super.setupEvents();
        this.listenFor(
            "create",
            event=>{
                this.loading()
                let formData = this.serializeForm(this.formTarget())
                this.post(
                    "/shops/upsert",
                    formData
                ).then(response=>{
                    this.loaded()
                    this.handleResponse(response,formData,`${formData.shopName} Created`)
                }).catch(error=>this.showError(error.message))
            }
        );
        this.listenFor(
            "update",
            event=>{
                this.loading()
                let formData = this.serializeForm(this.formTarget())
                this.post(
                    "/shops/upsert",
                    formData
                ).then(response=>{
                    this.loaded()
                    this.handleResponse(response,formData,`${formData.shopName} Updated`)
                }).catch(error=>this.showError(error.message))
            }
        );
        this.listenFor(
            "check-scopes",
            event=>{
                this.loading()
                this.get(`/shops/recheck/${this.objectId}`).then(response=>{
                    this.loaded();
                    switch(response.status) {
                        case 404:
                            this.showError(`
                                The credientials you have supplied are incomplete. Please make sure the following scopes are enabled:
                                <ul>${response.scopesMissing.map(scope=>`<li>${scope}</li>`).join("")}
                            `);
                        break;
                        case 200:
                            this.showMessage(`
                                ${response.shop.shopName} has all the required API scopes
                            `)
                        break;
                            
                }
            }).catch(error=>this.showError(error.message));
        })
        this.listenFor(
            "delete",
            event=>{
                this.loading()
                this.get(`/shops/delete/${this.objectId}`).then(response=>{
                    this.loaded()
                    this.showMessage(`Deleted ${this.shopDetails.shopName}`)
                    location.href="/shops"
                }).catch(error=>this.showError(error.message))
            }
        );
        this.listenFor(
            "theme-files",
            event=>{
                location.href=`/shops/${this.objectId}/deploy`
            }
        )
    }
    formHeader() {
        if (this.shopDetails.shopName) {
            return `Edit ${this.shopDetails.shopName}`
       } else {
           return `Create Shop`
       }
    }
    handleResponse(response,formData,message) {
        switch(response.status) {
            case 401:
                this.showError(`
                    The credentials you have supplied to ${formData.shopDomain}.myshopify.com are incorrect. Please check them and try again.
                `)
                break;
            case 404:
                this.objectId = response.shop.id
                this.showError(`
                    The credientials you have supplied are incomplete. Please make sure the following scopes are enabled:
                    <ul>${response.scopesMissing.map(scope=>`<li>${scope}</li>`).join("")}
                `)
                break;
            case 200:
                this.objectId = response.shopId
                this.shopDetails = response.shop
                history.replaceState(null, "", `/shops?shopId=${response.shopId}`);
                this.showMessage(message)
                this.render()
                break;
        }

    }
    setShopId(id) {
        if (id==null) {
            return
        }
        this.shopId = id;
        let form  = document.querySelector("#siteForm")
        let idInput = form.querySelector('[name="shopId]')
        
        if (idInput!=null) {
            idInput.value = id;
        } else {
            let input = document.createElement("input");
            input.type="hidden";
            input.name="shopId";
            input.value = id;
            form.appendChild(input)
        }

    }
}
