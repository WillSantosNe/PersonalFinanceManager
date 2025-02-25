# 📌 Implementação da CategoryViewSet

## **1️⃣ Criar os Serializers**
Teremos **dois serializers**:
- **`CategorySerializer`** → Usado por **usuários comuns**, exibindo apenas alguns campos do usuário.
- **`AdminCategorySerializer`** → Usado por **staffs**, exibindo todos os campos.

✅ **O que fazer?**
- `CategorySerializer` deve incluir `name`, `type`, e **apenas** `email`, `first_name`, `last_name` do dono da categoria.
- `AdminCategorySerializer` deve incluir **todos os campos** (incluindo `user`).

💡 **Dica**: Criar um **método `to_representation`** no `CategorySerializer` para manipular os dados do usuário e exibir apenas os campos permitidos.

---

## **2️⃣ Criar a `CategoryViewSet`**
A `CategoryViewSet` precisa respeitar regras de permissão para **visualização, criação, atualização e deleção**.

### **🟢 `get_serializer_class`**
✅ **O que fazer?**
- Se o usuário **for staff**, usar `AdminCategorySerializer`.
- Se o usuário **não for staff**, usar `CategorySerializer`.

💡 **Dica**:
- Utilize `self.request.user.is_staff` para verificar se o usuário pode acessar o serializer completo.

---

### **🟢 `get_queryset`**
✅ **O que fazer?**
- **Todos os usuários podem ver todas as categorias.**
- A diferença está nos **campos retornados** (controlado pelos serializers).

💡 **Dica**:
- Retornar `Category.objects.all()` para permitir a visualização global.

---

### **🟢 `perform_create`**
✅ **O que fazer?**
- Se o usuário **for staff**, permitir que ele escolha um `user` na criação da categoria.
- Se o usuário **não for staff**, **forçar** que a categoria seja criada **somente para ele mesmo**.

💡 **Dica**:
- Usar `serializer.save(user=self.request.user)` para garantir que um usuário comum crie categorias apenas para si mesmo.

---

### **🟢 `perform_update`**
✅ **O que fazer?**
- Se o usuário **for staff**, permitir **alterar qualquer categoria**.
- Se o usuário **não for staff**, permitir **alterar apenas `name` e `type`**.

💡 **Dica**:
- **Remover os campos proibidos** (`user`) antes de salvar os dados do usuário comum.

---

### **🟢 `perform_destroy`**
✅ **O que fazer?**
- Se o usuário **for staff**, permitir **deletar qualquer categoria**.
- Se o usuário **não for staff**, permitir **apenas deletar suas próprias categorias**.

💡 **Dica**:
- **Verificar se `instance.user == request.user` antes de permitir a exclusão.**
- Caso contrário, **lançar um `PermissionDenied`**.

---

## **📌 Resumo das Tarefas**
✅ **1. Criar os serializers:**
   - `CategorySerializer` (campos limitados para usuários comuns).
   - `AdminCategorySerializer` (todos os campos para staff).
   - **Usar `to_representation` para limitar a exibição do usuário.**

✅ **2. Criar a `CategoryViewSet`:**
   - **`get_serializer_class`** → Definir o serializer correto com base no tipo de usuário.
   - **`get_queryset`** → Permitir a visualização de todas as categorias, com diferença nos campos exibidos.
   - **`perform_create`** → Staff pode criar para qualquer usuário, usuário comum apenas para si mesmo.
   - **`perform_update`** → Staff pode mudar tudo, usuário comum apenas `name` e `type`.
   - **`perform_destroy`** → Staff pode deletar qualquer categoria, usuário comum apenas a própria.

---

### 🚀 **Agora é sua vez de implementar!**

