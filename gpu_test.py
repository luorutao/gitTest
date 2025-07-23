import torch
import time

# Dummy model and data
model = torch.nn.Linear(1000, 1000)
data = torch.randn(1000, 1000)
target = torch.randn(1000, 1000)
loss_fn = torch.nn.MSELoss()

def test_device(device_name):
    device = torch.device(device_name)
    model_d = model.to(device)
    data_d = data.to(device)
    target_d = target.to(device)
    
    optimizer = torch.optim.SGD(model_d.parameters(), lr=0.01)

    start = time.time()
    for _ in range(1000):  # Run 100 iterations
        optimizer.zero_grad()
        output = model_d(data_d)
        loss = loss_fn(output, target_d)
        loss.backward()
        optimizer.step()
    end = time.time()
    
    print(f"{device_name} elapsed time: {end - start:.2f} seconds")

# Run tests
print("Testing elapsed time...")
test_device("cpu")

if torch.backends.mps.is_available():
    test_device("mps")
else:
    print("MPS not available on this system.")
