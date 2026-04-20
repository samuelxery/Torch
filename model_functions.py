import torch
from torch import nn
from helper_functions import accuracy_fn
def get_model_results(model: nn.Module, loader: torch.utils.data.DataLoader, loss_function, device='cpu'):
    """Function made by the gremory that gives model loss and accuracy on given dataloader in form of dicktionary"""
    loss, acc = 0, 0
    model.eval()
    with torch.inference_mode():
        for x, y in loader:
            x, y = x.to(device), y.to(device)
            pred = model(x)
            loss += loss_function(pred, y)
            acc += accuracy_fn(y, pred.argmax(dim=1))
        loss /= len(loader)
        acc /= len(loader)
        return {"Loss: ": loss.item(),
                "accuracy": acc,
                "model": model.__class__.__name__}
def training_epoch(model, device, dataloader, optimizer, criterion):
    train_loss = 0
    for batch, (x, y) in enumerate(dataloader):
        x, y = x.to(device), y.to(device)
        model.train()
        pred = model(x)
        loss = criterion(pred, y)
        train_loss += loss
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        if batch % 400 == 0:
            print(f"we at batch: {batch * len(x)}/{len(dataloader.dataset)}")
    train_loss /= len(dataloader)
    return train_loss
def testing_epoch(model, device, dataloader, criterion, accuracy_fn):
    test_loss = 0
    test_acc = 0
    model.eval()
    with torch.no_grad():
        for x, y in dataloader:
            x, y = x.to(device), y.to(device)
            pred = model(x)
            test_loss += criterion(pred, y)
            test_acc += accuracy_fn(y_true=y, y_pred=pred.argmax(dim=1))
        test_loss /= len(dataloader)
        test_acc /= len(dataloader)
    print(f"\ntest_loss: {test_loss:.4f}, test_acc: {test_acc:.4}")
    return test_loss, test_acc





# ...existing code...
from tqdm import tqdm
from torch.utils.tensorboard import SummaryWriter

# create writer once and close after training (not every epoch)
writer = SummaryWriter(log_dir='runs')



# ...existing code...
def evaluate_model(model, loader, device):
    """Calculates the accuracy of the model on the test/validation set."""
    model.eval() # Set model to evaluation mode
    correct = 0
    total = 0
    with torch.no_grad():
        for inputs, targets in loader:
            inputs, targets = inputs.to(device), targets.to(device)
            outputs = model(inputs)
            _, predicted = outputs.max(1)
            total += targets.size(0)
            correct += predicted.eq(targets).sum().item()
    
    accuracy = 100. * correct / total
    return accuracy

def train_model(model, train_loader, test_loader, criterion, optimizer, scheduler, num_epochs, device):
    best_acc = 0.0
    print(f"Starting training on {device}...")

    for epoch in range(num_epochs):
        model.train()
        train_loss = 0
        correct = 0
        total = 0

        train_bar = tqdm(train_loader, desc=f"Epoch {epoch+1}/{num_epochs}")

        for batch_idx, (inputs, targets) in enumerate(train_bar):
            inputs, targets = inputs.to(device), targets.to(device)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()

            # step scheduler per batch if appropriate
            scheduler.step()

            train_loss += loss.item()
            _, predicted = outputs.max(1)
            total += targets.size(0)
            correct += predicted.eq(targets).sum().item()

            train_bar.set_postfix({
                'Loss': f'{train_loss/(batch_idx+1):.4f}',
                'Acc': f'{100.*correct/total:.2f}%',
                'LR': f'{optimizer.param_groups[0]["lr"]:.6f}'
            })

        # Evaluate on the test set after each epoch
        test_acc = evaluate_model(model, test_loader, device)
        print(f"Test Accuracy after Epoch {epoch+1}: {test_acc:.2f}%")
        writer.add_scalar('Epoch/acc', test_acc, epoch)
        # DO NOT close writer here

        if test_acc > best_acc:
            best_acc = test_acc
            print(f"** New best model saved with accuracy: {best_acc:.2f}% **")
            # save checkpoint if desired

    # close writer after training completes
    writer.close()
    torch.cuda.empty_cache()
    print(f"\nTraining complete. Best Test Accuracy: {best_acc:.2f}%")
# ...existing code...