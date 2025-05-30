import cocotb
from cocotb.clock import Clock
from cocotb.triggers import (
    RisingEdge, FallingEdge,
    Timer, ReadOnly
)
import random
from cocotb.result import TestFailure

DATA_WIDTH = 8
DEPTH = 8

############################# RESET VALUES #############################
async def reset_fifo(dut):
    dut.wrst_n.value = 0
    dut.rrst_n.value = 0
    dut.w_en.value = 0
    dut.r_en.value = 0
    dut.data_in.value = 0
    await Timer(50, units="ns")
    dut.wrst_n.value = 1
    dut.rrst_n.value = 1
    await RisingEdge(dut.wclk)
    await RisingEdge(dut.rclk)
    

############################# WRITE VALUES #############################
async def writer(dut, test_data):
    for val in test_data:
        while dut.full.value:
            await RisingEdge(dut.wclk)
        dut.data_in.value = val
        dut.w_en.value = 1
        await RisingEdge(dut.wclk)
        dut.w_en.value = 0
        # await Timer(random.randint(10, 20), units="ns")
        await RisingEdge(dut.wclk)
        

############################# READ VALUES #############################
async def reader(dut, num_items, expected_data):
    read_data = []
    await Timer(100, units="ns")  # Delay to allow writes to get started

    for _ in range(num_items):
        while dut.empty.value:
            await RisingEdge(dut.rclk)

        # Assert read enable
        dut.r_en.value = 1
        await RisingEdge(dut.rclk)
        dut.r_en.value = 0

        # Wait one more cycle to allow data_out to update
        await RisingEdge(dut.rclk)
        await ReadOnly()

        # Check if data_out is valid
        raw_val = dut.data_out.value
        if not raw_val.is_resolvable:
            raise TestFailure(f"data_out is unresolvable (x/z): {raw_val}")

        read_val = raw_val.integer
        read_data.append(read_val)

        # Add randomized delay to simulate realistic async read behavior
        await Timer(random.randint(5, 20), units="ns")

    assert read_data == expected_data, f"Mismatch! Expected {expected_data}, got {read_data}"



############################# MAIN TESTS #############################
@cocotb.test()
async def template_test(dut):
    
	cocotb.start_soon(Clock(dut.rclk, 13, units='ns').start())
	cocotb.start_soon(Clock(dut.wclk, 7, units='ns').start())

	await reset_fifo(dut)
    
	test_data = [random.randint(0, 255) for _ in range(8)]
     
	await cocotb.start(writer(dut, test_data))
	await cocotb.start(reader(dut, len(test_data), test_data))

	await Timer(2000, units="ns")

